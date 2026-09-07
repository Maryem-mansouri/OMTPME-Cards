import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_SENDER_NAME = os.environ.get("SMTP_SENDER_NAME", "Plateforme OMTPME")


def send_password_changed_email(to_email):
    """Envoie un email de confirmation après un changement de mot de passe
    réussi. Ne bloque jamais l'app même si l'envoi échoue."""
    if not SMTP_USER or not SMTP_PASSWORD:
        print("SMTP non configuré (SMTP_USER/SMTP_PASSWORD manquants) — email non envoyé.")
        return False

    subject = "Votre mot de passe a été modifié"
    body = (
        "Bonjour,\n\n"
        "Nous vous confirmons que le mot de passe de votre compte sur la "
        "Plateforme des Cartes OMTPME vient d'être modifié avec succès.\n\n"
        "Si vous n'êtes pas à l'origine de ce changement, contactez "
        "immédiatement l'administrateur de la plateforme.\n\n"
        "— OMTPME"
    )

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = f"{SMTP_SENDER_NAME} <{SMTP_USER}>"
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())
        print(f"Email de confirmation envoyé avec succès à {to_email}")
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False