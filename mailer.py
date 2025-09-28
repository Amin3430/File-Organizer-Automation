import smtplib
from email.message import EmailMessage
import json, os
from utils import now_str

def load_smtp():
    cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg.get("smtp", {})

def send_report(subject, body, attach_path=None):
    smtp = load_smtp()
    if not smtp:
        raise RuntimeError("SMTP config not set in config.json")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp.get("from_addr")
    msg["To"] = smtp.get("to_addr")
    msg.set_content(body)
    if attach_path and os.path.exists(attach_path):
        with open(attach_path, "rb") as f:
            data = f.read()
        msg.add_attachment(data, maintype="application", subtype="zip", filename=os.path.basename(attach_path))
    with smtplib.SMTP(smtp.get("host"), smtp.get("port")) as s:
        s.starttls()
        s.login(smtp.get("username"), smtp.get("password"))
        s.send_message(msg)
    return True
