# api/app/routes_vendor.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import os, zipfile, glob, time, subprocess, shutil

from .utils_email import send_email  # fill SMTP creds in that file

router = APIRouter(prefix="/vendor", tags=["vendor"])

CATALOG_DIR = "./data"
OUTPUT_ROOT = "./data/vendor_packages"

class VendorLine(BaseModel):
    code: str
    qty: int

class VendorPackageRequest(BaseModel):
    po_id: str
    vendor_name: str
    lines: List[VendorLine]
    combine_pdf: bool = True
    email_to: Optional[str] = None
    email_subject: Optional[str] = None
    email_body: Optional[str] = None

def combine_pngs_to_pdf(png_folder: str, out_pdf_path: str):
    # use PyMuPDF if available; otherwise PIL fallback
    try:
        import fitz  # PyMuPDF
        doc = fitz.open()
        pngs = sorted(glob.glob(os.path.join(png_folder, "*.png")))
        for p in pngs:
            img = fitz.open(p)
            rect = img[0].rect
            pdfbytes = img.convert_to_pdf()
            imgpdf = fitz.open("pdf", pdfbytes)
            page = doc.new_page(width=rect.width, height=rect.height)
            page.show_pdf_page(rect, imgpdf, 0)
        doc.save(out_pdf_path)
        doc.close()
    except Exception:
        from PIL import Image
        pngs = sorted(glob.glob(os.path.join(png_folder, "*.png")))
        if not pngs:
            raise RuntimeError("No PNGs to combine")
        images = [Image.open(p).convert("RGB") for p in pngs]
        head, *tail = images
        head.save(out_pdf_path, save_all=True, append_images=tail)

@router.post("/generate-package")
def generate_vendor_package(req: VendorPackageRequest, bg: BackgroundTasks):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder = os.path.join(OUTPUT_ROOT, f"{req.vendor_name}_PO{req.po_id}_{timestamp}")
    os.makedirs(folder, exist_ok=True)

    # Build --lines param like "SI-001:10,SI-002:5"
    lines_arg = ",".join([f"{l.code}:{l.qty}" for l in req.lines])

    # call existing PDF → annotated PNG generator
    cmd = [
        "python", "scripts/generate_vendor_images.py",
        "--po-id", str(req.po_id),
        "--vendor", req.vendor_name,
        "--lines", lines_arg,
        "--catalog-dir", CATALOG_DIR,
        "--out-dir", folder
    ]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        raise HTTPException(500, f"Image generation failed: {e}")

    zip_path = os.path.join(folder, "package_images.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in glob.glob(os.path.join(folder, "*.png")):
            z.write(f, arcname=os.path.basename(f))

    pdf_path = None
    if req.combine_pdf:
        pdf_path = os.path.join(folder, "package_combined.pdf")
        combine_pngs_to_pdf(folder, pdf_path)

    # Email (optional)
    if req.email_to:
        attachments = []
        if req.combine_pdf and pdf_path and os.path.exists(pdf_path):
            attachments.append(pdf_path)
        else:
            attachments.append(zip_path)
        subject = req.email_subject or f"Asaani Vendor Package — PO {req.po_id} ({req.vendor_name})"
        body = req.email_body or "Please find the marked items attached."
        # offload to background so API returns quick
        bg.add_task(send_email, to=req.email_to, subject=subject, body=body, attachments=attachments)

    return {
        "status": "success",
        "out_dir": folder.replace("\\", "/"),
        "zip": zip_path.replace("\\", "/"),
        "pdf": (pdf_path.replace("\\", "/") if pdf_path else None)
    }
