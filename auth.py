import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = "users.json"

# ===== EMAILS AUTORISÉS =====
ALLOWED_EMAILS = [
    "m.elmansouri@omtpme.ma",
    "r.bennouna@omtpme.ma",
    "s.skhoun@omtpme.ma",
    "r.sahmi@omtpme.ma",
    "s.bouziane@omtpme.ma",
    "ne.azekri@omtpme.ma"
    
]

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def is_email_allowed(email):
    return email.strip().lower() in [e.lower() for e in ALLOWED_EMAILS]

def register_user(email, password):
    users = load_users()
    email = email.strip().lower()
    if email in users:
        return False, "Cet email a déjà un compte."
    users[email] = generate_password_hash(password)
    save_users(users)
    return True, "Compte créé avec succès."

def verify_user(email, password):
    users = load_users()
    email = email.strip().lower()
    if email not in users:
        return False, "Email non trouvé. Créez d'abord votre compte."
    if check_password_hash(users[email], password):
        return True, "Connexion réussie."
    return False, "Mot de passe incorrect."