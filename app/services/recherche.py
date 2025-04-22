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
def send_friend_request(user_id_from, user_id_to):
    if user_id_from == user_id_to:
        print("Impossible d’envoyer une demande à soi-même.")
        return

    cursor = mysql.connection.cursor()

    # Vérifie si une relation existe déjà dans un sens ou dans l'autre
    check_query = """
        SELECT 1 FROM amis
        WHERE (user_id_1 = %s AND user_id_2 = %s)
           OR (user_id_1 = %s AND user_id_2 = %s)
    """
    cursor.execute(check_query, (user_id_from, user_id_to, user_id_to, user_id_from))
    existing = cursor.fetchone()

    if not existing:
        insert_query = """
            INSERT INTO amis (user_id_1, user_id_2, statut)
            VALUES (%s, %s, 'pending')
        """
        try:
            cursor.execute(insert_query, (user_id_from, user_id_to))
            mysql.connection.commit()
            print("Demande d'ami insérée dans la base de données.")
        except Exception as e:
            print("Erreur lors de l'insertion :", e)
            mysql.connection.rollback()
    else:
        print("Une relation existe déjà entre ces deux utilisateurs.")

    cursor.close()