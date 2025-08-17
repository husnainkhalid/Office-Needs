# api/app/utils_email.py
import smtplib, os, mimetypes
from email.message import EmailMessage

SMTP_HOST = os.getenv("ASAANI_SMTP_HOST", "smtp.yourprovider.com")
SMTP_PORT = int(os.getenv("ASAANI_SMTP_PORT", "587"))
SMTP_USER = os.getenv("ASAANI_SMTP_USER", "husnainkhalid1@gmail.com")
SMTP_PASS = os.getenv("ASAANI_SMTP_PASS", "01010101")
SMTP_FROM = os.getenv("ASAANI_SMTP_FROM", "Asaani <noreply@example.com>")

def send_email(to: str, subject: str, body: str, attachments=None):
    msg = EmailMessage()
    msg["From"] = SMTP_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    for path in attachments or []:
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(path, "rb") as f:
            msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(path))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
