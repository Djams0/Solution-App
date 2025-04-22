from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from flask import session
from app import mysql
import base64
import os
import json
from datetime import datetime

def send_message(destinataire_id, message_clair):
    cursor = mysql.connection.cursor()

    # Récupérer la clé publique du destinataire
    cursor.execute("SELECT public_key, username FROM users WHERE id = %s", (destinataire_id,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        return False, "Utilisateur non trouvé."

    public_key_pem = result[0].encode()
    destinataire_username = result[1]
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Chiffrer le message
    message_chiffre = public_key.encrypt(
        message_clair.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Encodage base64 pour stockage texte
    message_b64 = base64.b64encode(message_chiffre).decode()

    # Sauvegarde dans la base de données
    cursor.execute("""
        INSERT INTO messages (expediteur_id, destinataire_id, message_chiffre)
        VALUES (%s, %s, %s)
    """, (session['user_id'], destinataire_id, message_b64))
    mysql.connection.commit()
    cursor.close()

    # Sauvegarde locale du message en clair
    message_data = {
        "destinataire_id": destinataire_id,
        "destinataire_username": destinataire_username,
        "message": message_clair,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")  # format BDD
    }


    fichier = f"local_storage/messages_envoyes_{session['username']}.json"
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            historique = json.load(f)
    else:
        historique = []

    historique.append(message_data)

    os.makedirs("local_storage", exist_ok=True)
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)

    return True, "Message envoyé avec succès"


def get_messages(ami_id):
    cursor = mysql.connection.cursor()
    user_id = session['user_id']

    cursor.execute("""
        SELECT expediteur_id, message_chiffre, timestamp
        FROM messages
        WHERE (expediteur_id = %s AND destinataire_id = %s)
           OR (expediteur_id = %s AND destinataire_id = %s)
        ORDER BY timestamp ASC
    """, (user_id, ami_id, ami_id, user_id))
    rows = cursor.fetchall()
    cursor.close()

    messages = []

    # Charger la clé privée de l'utilisateur courant
    key_path = f"private_keys/{session['username']}_private_key.pem"
    with open(key_path, "rb") as f:
        private_key_pem = f.read()

    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=os.getenv("PRIVATE_KEY_PASSWORD", "defaultpassword").encode()
    )

    # Charger l'historique des messages envoyés en clair
    fichier = f"local_storage/messages_envoyes_{session['username']}.json"
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            historique = json.load(f)
    else:
        historique = []

    # Filtrer les messages envoyés à l'ami spécifié
    for msg in historique:
        if msg['destinataire_id'] == ami_id:
            messages.append({
                'expediteur_id': session['user_id'],
                'contenu': msg['message'],
                'timestamp': msg['timestamp']
            })

    # Déchiffrer les messages reçus de l'ami
    for row in rows:
        expediteur_id, message_b64, timestamp = row

        # Ignorer les messages déjà ajoutés depuis l'historique local
        if expediteur_id == user_id:
            continue

        message_clair = "[Impossible de déchiffrer]"

        try:
            message_bytes = base64.b64decode(message_b64)
            message_clair = private_key.decrypt(
                message_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ).decode()
        except Exception:
            pass  # Laisser "Impossible de déchiffrer" si le déchiffrement échoue

        messages.append({
            'expediteur_id': expediteur_id,
            'contenu': message_clair,
            'timestamp': timestamp
        })

    return messages
