from app import mysql

# Recherche un utilisateur par son nom d'utilisateur exact
def search_user(username):
    cursor = mysql.connection.cursor()
    query = "SELECT id, username FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    results = cursor.fetchall()
    cursor.close()

    users = [{'id': row[0], 'username': row[1]} for row in results]
    return users

# Envoie une demande d'amitié
def send_friend_request(sender_id, receiver_id):
    """
    Envoie une demande d'amitié d'un utilisateur à un autre.
    :param sender_id: ID de l'utilisateur qui envoie la demande
    :param receiver_id: ID de l'utilisateur qui reçoit la demande
    :return: Tuple (success, message)
    """
    print("Module reseau importé avec succès")

    cursor = None
    try:
        # Récupération de la connexion MySQL depuis Flask app context
        db = mysql
        cursor = db.connection.cursor()

        # Vérifie si une relation existe déjà
        cursor.execute("""
            SELECT 1 FROM amis
            WHERE 
                (user_id_1 = %s AND user_id_2 = %s)
                OR (user_id_1 = %s AND user_id_2 = %s)
        """, (sender_id, receiver_id, receiver_id, sender_id))

        if cursor.fetchone():
            return False, "Une relation existe déjà entre ces utilisateurs."

        # Crée une nouvelle demande d'amitié avec le statut 'pending'
        cursor.execute("""
            INSERT INTO amis (user_id_1, user_id_2, statut, date_amitie)
            VALUES (%s, %s, %s, NOW())
        """, (sender_id, receiver_id, 'pending'))

        db.connection.commit()
        return True, "Demande d'amitié envoyée avec succès."

    except Exception as e:
        if db:
            db.connection.rollback()
        return False, f"Erreur lors de l'envoi de la demande : {str(e)}"

    finally:
        if cursor:
            cursor.close()
