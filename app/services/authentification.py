import bcrypt
import os
from dotenv import load_dotenv
from flask import session
from app import mysql
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

load_dotenv()

class AuthService:
    def __init__(self, mysql):
        self.mysql = mysql

    def register_user(self, username, password):
        cursor = mysql.connection.cursor()

        # Vérifie si l'utilisateur existe déjà
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return False, "Nom d'utilisateur déjà utilisé"

        # Hasher le mot de passe avec pepper
        pepper = os.getenv("PEPPER", "")
        peppered_password = password + pepper
        hashed_pw = bcrypt.hashpw(peppered_password.encode('utf-8'), bcrypt.gensalt())

        # Génération de la paire de clés RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        # Sérialisation de la clé publique (format PEM)
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        # Sérialisation de la clé privée (avec chiffrement)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                os.getenv("PRIVATE_KEY_PASSWORD", "defaultpassword").encode()
            )
        )

        # Création du dossier pour stocker les clés privées
        key_dir = "private_keys"
        os.makedirs(key_dir, exist_ok=True)

        # Sauvegarde dans un fichier sécurisé
        with open(f"{key_dir}/{username}_private_key.pem", "wb") as f:
            f.write(private_pem)

        # Insertion dans la base de données (seulement la clé publique)
        cursor.execute("INSERT INTO users (username, password, public_key) VALUES (%s, %s, %s)",
                    (username, hashed_pw, public_pem))
        mysql.connection.commit()

        # Récupère l'ID de l'utilisateur
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]
        cursor.close()

        # Stocke les infos dans la session
        session['user_id'] = user_id
        session['username'] = username

        return True, "Utilisateur créé avec succès"


    def authenticate_user(self, username, password):
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            user_id, username_db, hashed_pw = user

            pepper = os.getenv("PEPPER", "")
            peppered_password = password + pepper

            if bcrypt.checkpw(peppered_password.encode('utf-8'), hashed_pw):
                return {
                    'id': user_id,
                    'username': username_db
                }

        return None
