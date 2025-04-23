from app import mysql

class HomeService:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_user_friends(self, user_id):
        cursor = mysql.connection.cursor()

        query = """
                    SELECT 
                u.id, u.username, a.statut, a.date_amitie
            FROM amis a
            JOIN users u ON 
                (a.user_id_1 = %s AND u.id = a.user_id_2)
                OR (a.user_id_2 = %s AND u.id = a.user_id_1)
            WHERE (a.user_id_1 = %s OR a.user_id_2 = %s)
            AND a.statut = 'accept'
            ORDER BY 
                a.date_amitie DESC;

        """
        cursor.execute(query, (user_id, user_id, user_id, user_id))
        results = cursor.fetchall()
        cursor.close()

        friends = []
        for row in results:
            user_id, username, statut, date_amitie = row
            friends.append({
                'id': user_id,
                'username': username,
                'statut': statut,
                'date_amitie': date_amitie
            })

        return friends
