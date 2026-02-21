from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Database Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['arredamento_db']

# Admin Data
email_admin = "adminMarco@arredamento.it"
pass_admin = "adminMarco2026"

# Create Admin User

db.utenti.update_one(
    {"email": email_admin}, 
    {
        "$set": {
            "nome": "Amministratore",
            "email": email_admin,
            "password": generate_password_hash(pass_admin), # cript password
            "ruolo": "admin"  
        }
    },
    upsert=True
)

print(f" Utente Admin creato con successo!")
print(f"Email: {email_admin}")
print(f"Password: {pass_admin}")