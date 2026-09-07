import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_SENDER_NAME = os.environ.get("SMTP_SENDER_NAME", "Plateforme OMTPME")

def send_password_changed_email(to_email):
    if not SMTP_USER or not SMTP_PASSWORD:
        print("SMTP non configuré (SMTP_USER/SMTP_PASSWORD manquants) — email non envoyé.", flush=True)
        return False

    ...

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())
        print(f"Email de confirmation envoyé avec succès à {to_email}", flush=True)
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}", flush=True)
        return False