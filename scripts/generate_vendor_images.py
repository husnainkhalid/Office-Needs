import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import os
import argparse

def generate_images(po_id, vendor, lines, catalog_dir, output_dir=None):
    """
    po_id: Purchase Order ID
    vendor: Vendor name
    lines: list of dicts [{"code": "SI-1234", "qty": 10}]
    catalog_dir: folder containing PDFs
    """
    if output_dir is None:
        output_dir = os.path.join(catalog_dir, f"vendor_order_{vendor}_PO{po_id}")
    os.makedirs(output_dir, exist_ok=True)

    font = ImageFont.load_default()

    # iterate through PDF files
    for pdf_file in os.listdir(catalog_dir):
        if not pdf_file.lower().endswith(".pdf"):
            continue
        pdf_path = os.path.join(catalog_dir, pdf_file)
        doc = fitz.open(pdf_path)
        for page_no, page in enumerate(doc):
            text = page.get_text()
            for line in lines:
                code = line["code"]
                qty = line["qty"]
                if code in text:
                    # get bbox of text
                    for inst in page.search_for(code):
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        draw = ImageDraw.Draw(img)
                        # rectangle around code
                        x0, y0, x1, y1 = inst
                        draw.rectangle([x0, y0, x1, y1], outline="red", width=5)
                        # draw quantity circle
                        radius = 30
                        circle_x = x1 + radius
                        circle_y = y0
                        draw.ellipse([circle_x, circle_y, circle_x + radius*2, circle_y + radius*2], outline="red", width=5)
                        draw.text((circle_x + 10, circle_y + 10), str(qty), fill="red", font=font)
                        # save image
                        img_path = os.path.join(output_dir, f"{code}_page{page_no+1}.png")
                        img.save(img_path)
                        print(f"Generated {img_path}")
    print("All images generated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Vendor Images from PDFs")
    parser.add_argument("--po-id", type=int, required=True)
    parser.add_argument("--vendor", type=str, required=True)
    parser.add_argument("--lines-file", type=str, help="CSV with code,qty")
    parser.add_argument("--catalog-dir", type=str, required=True)
    args = parser.parse_args()

    lines = []
    if args.lines_file:
        import csv
        with open(args.lines_file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lines.append({"code": row["code"], "qty": int(row["qty"])})
    else:
        # example placeholder lines
        lines = [{"code": "SI-1234", "qty": 10}, {"code": "SI-5678", "qty": 5}]

    generate_images(args.po_id, args.vendor, lines, args.catalog_dir)
