from app import mysql


class MesReseauxService:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_pending_requests(self, user_id):
        cursor = mysql.connection.cursor()

        # Demandes envoyées
        query_sent = """
            SELECT 
                u.id, u.username, a.date_amitie
            FROM amis a
            JOIN users u ON a.user_id_2 = u.id
            WHERE a.user_id_1 = %s
            AND a.statut = 'pending'
            ORDER BY a.date_amitie DESC
        """
        cursor.execute(query_sent, (user_id,))
        sent_results = cursor.fetchall()

        # Demandes reçues
        query_received = """
            SELECT 
                u.id, u.username, a.date_amitie
            FROM amis a
            JOIN users u ON a.user_id_1 = u.id
            WHERE a.user_id_2 = %s
            AND a.statut = 'pending'
            ORDER BY a.date_amitie DESC
        """
        cursor.execute(query_received, (user_id,))
        received_results = cursor.fetchall()
        
        cursor.close()

        demandes_envoyees = [{
            'id': row[0],
            'username': row[1],
            'date_amitie': row[2]
        } for row in sent_results]

        demandes_recues = [{
            'id': row[0],
            'username': row[1],
            'date_amitie': row[2]
        } for row in received_results]

        return {
            'envoyees': demandes_envoyees,
            'recues': demandes_recues
        }
        
        
        
        
    def update_friend_request_status(self, user_id_1, user_id_2, action):
        cursor = mysql.connection.cursor()
        statut = 'accept' if action == 'accept' else 'reject'

        # Mettre à jour le statut de la demande
        query = """
            UPDATE amis 
            SET statut = %s
            WHERE (user_id_1 = %s AND user_id_2 = %s) OR (user_id_1 = %s AND user_id_2 = %s)
        """
        cursor.execute(query, (statut, user_id_1, user_id_2, user_id_2, user_id_1))
        mysql.connection.commit()
        cursor.close()
