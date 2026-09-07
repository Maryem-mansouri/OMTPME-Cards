import os
import requests

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
SMTP_SENDER_NAME = os.environ.get("SMTP_SENDER_NAME", "OMTPME")


def send_password_changed_email(to_email):
    """Envoie un email de confirmation via l'API HTTP de Resend
    (le SMTP classique est bloqué sur Hugging Face Spaces)."""
    if not RESEND_API_KEY:
        print("RESEND_API_KEY manquante — email non envoyé.", flush=True)
        return False

    payload = {
        "from": f"{SMTP_SENDER_NAME} <onboarding@resend.dev>",
        "to": [to_email],
        "subject": "Votre mot de passe a été modifié",
        "text": (
            "Bonjour,\n\n"
            "Nous vous confirmons que le mot de passe de votre compte sur la "
            "Plateforme des Cartes OMTPME vient d'être modifié avec succès.\n\n"
            "Si vous n'êtes pas à l'origine de ce changement, contactez "
            "immédiatement l'administrateur de la plateforme.\n\n"
            "— OMTPME"
        ),
    }

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=10,
        )
        if response.status_code in (200, 201):
            print(f"Email de confirmation envoyé avec succès à {to_email}", flush=True)
            return True
        else:
            print(f"Erreur envoi email: {response.status_code} - {response.text}", flush=True)
            return False
    except Exception as e:
        print(f"Erreur envoi email: {e}", flush=True)
        return False