import os
from flask import session
from app import mysql
from app.services.authentification import AuthService
from app.services.home import HomeService
from app.services.mes_reseaux import MesReseauxService
from app.services.recherche import RechercheService

class BaseUser:
    def __init__(self, mysql):
        self.mysql = mysql


class User(BaseUser):
    def __init__(self, mysql):
        super().__init__(mysql)
        self.auth_service = AuthService(mysql)
        self.network_service = MesReseauxService(mysql)
        self.friends_service = HomeService(mysql)
        self.search_service = RechercheService(mysql)

    # Authentification
    def register(self, username, password):
        return self.auth_service.register_user(username, password)

    def login(self, username, password):
        return self.auth_service.authenticate_user(username, password)

    # Récupération des amis
    def get_friends(self, user_id):
        return self.friends_service.get_user_friends(user_id)

    # Réseau : demandes d'amitié
    def get_pending_requests(self, user_id):
        return self.network_service.get_pending_requests(user_id)

    def update_friend_status(self, user_id_1, user_id_2, action):
        return self.network_service.update_friend_request_status(user_id_1, user_id_2, action)

    # Recherche et invitation
    def search_users(self, username):
        return self.search_service.search_user(username)

    def send_friend_request(self, user_id_from, user_id_to):
        return self.search_service.send_friend_request(user_id_from, user_id_to)
