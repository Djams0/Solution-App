## Secure Messaging Application
# Description
Ce projet est une application de messagerie sécurisée utilisant un chiffrement de bout en bout basé sur RSA. Les utilisateurs peuvent envoyer des messages chiffrés qui ne peuvent être lus que par le destinataire, garantissant ainsi la confidentialité des échanges. L'application propose également un système d'authentification robuste, un stockage sécurisé des clés privées, ainsi qu'une interface simple pour envoyer et recevoir des messages.

Les utilisateurs peuvent également :

# Ajouter des amis via un système de recherche basé sur leur username.


## Fonctionnalités principales
Chiffrement de bout en bout avec RSA pour garantir la confidentialité des messages.

Authentification sécurisée avec mot de passe haché et salé via bcrypt.

Stockage des clés privées sur l'appareil client pour garantir la sécurité des utilisateurs.

Base de données MySQL pour stocker les informations des utilisateurs et les clés publiques.

Interface utilisateur simple en utilisant HTML, CSS et Flask.

Gestion des amis : Recherche d'amis via le username, ajout d'amis, et démarrage de conversations sécurisées.

## Technologies utilisées
Langages : Python, HTML, CSS

Framework web : Flask

Base de données : MySQL

Chiffrement : Bibliothèque cryptography pour RSA et AES

Sécurité : bcrypt pour le hachage des mots de passe

Sessions utilisateur : Flask-Session pour la gestion des sessions

Environnement de développement : Virtualenv (venv)

## Architecture du projet

app/
│
├── services/
│   ├── authentification.py
│   ├── chat.py
│   ├── home.py
│   ├── mes_reseaux.py
│   └── recherche.py
│
├── static/          # Contient les fichiers CSS et JS
│
├── templates/       # Contient les fichiers HTML
│
├── __init__.py      # Initialisation de l'application Flask
├── config.py        # Configuration de l'application (base de données, clés secrètes)
├── routes.py        # Définition des routes Flask
│
├── flask_session/   # Gestion des sessions Flask
│
├── local_storage/   # Dossier pour stocker les messages envoyés localement
│
├── private_keys/    # Stockage des clés privées des utilisateurs
│
├── .env             # Variables d'environnement
├── requirements.txt # Liste des dépendances
├── run.py           # Point d'entrée pour exécuter l'application
│
venv/                # Environnement virtuel
## Dépendances
Installer les dépendances
Avant de faire tourner l'application, il faut installer les dépendances nécessaires. Voici les étapes :

Créer un environnement virtuel (si ce n’est pas déjà fait) :

python3 -m venv venv
Activer l'environnement virtuel :

Sur macOS/Linux :

source venv/bin/activate
Sur Windows :


.\venv\Scripts\activate
Installer les dépendances :


pip install -r requirements.txt

Configurer les variables d’environnement : Dans le fichier .env, ajoute les variables nécessaires comme suit :


DATABASE_HOST=localhost
DATABASE_USER=ton_utilisateur
DATABASE_PASSWORD=ton_mot_de_passe
DATABASE_NAME=nom_de_ta_bdd
SECRET_KEY=ta_clé_secrète
# Lancer l'application : Une fois les dépendances installées et les variables d'environnement configurées, tu peux démarrer l'application avec la commande suivante :


python run.py
Fonctionnalités
1. Chiffrement RSA
Les messages envoyés sont chiffrés avec la clé publique du destinataire et ne peuvent être déchiffrés qu'avec la clé privée correspondante. Ce mécanisme garantit que seuls le destinataire et l'expéditeur peuvent lire les messages échangés.

Génération des clés : Chaque utilisateur génère une paire de clés (publique et privée) lors de son inscription.

Chiffrement/déchiffrement des messages : Les messages sont chiffrés avant d'être envoyés et déchiffrés lorsque le destinataire les reçoit.

2. Authentification des utilisateurs
Lors de l'inscription et de la connexion, les mots de passe sont hachés et salés avec bcrypt pour assurer la sécurité des informations d'identification.

Hachage et salage des mots de passe : Les mots de passe sont transformés en une chaîne de caractères irréversible, ce qui empêche un attaquant de retrouver le mot de passe en cas de fuite de données.

Vérification du mot de passe : Lors de la connexion, le mot de passe saisi est comparé avec le hachage stocké en base de données.

3. Gestion des sessions
Les sessions sont gérées par Flask-Session, ce qui permet de maintenir l'état de l'utilisateur entre les différentes requêtes HTTP.

Stockage des sessions : Les sessions sont stockées côté serveur, ce qui évite d'exposer les informations sensibles dans les cookies du client.

4. Base de données MySQL
Les informations des utilisateurs (comme leurs clés publiques) sont stockées dans une base de données MySQL sécurisée.

Stockage des clés publiques : Chaque utilisateur a sa clé publique stockée dans la base de données.

Gestion des utilisateurs : Les informations des utilisateurs (nom, adresse e-mail, mot de passe haché) sont également stockées dans la base de données.

5. Fonctionnalité de recherche d'amis
Les utilisateurs peuvent rechercher d'autres utilisateurs par username et leur envoyer une demande d'ami.

Recherche par username : Un utilisateur peut rechercher un autre utilisateur en utilisant son username dans la barre de recherche.

Ajout d'amis : Lorsqu'un utilisateur trouve un autre utilisateur, il peut l'ajouter à sa liste d'amis.

6. Discussions avec les amis
Une fois qu'un utilisateur a ajouté un autre utilisateur comme ami, ils peuvent démarrer une conversation privée.

Envoi de messages : L'utilisateur peut envoyer des messages chiffrés à ses amis.

Affichage des conversations : Les messages sont affichés de manière sécurisée dans la fenêtre de conversation avec l'ami concerné.

## Choix techniques
Flask : Un framework léger et flexible pour le développement d'applications web en Python. Nous l'avons choisi pour sa simplicité et sa facilité d'intégration avec d'autres bibliothèques comme cryptography.

Cryptography (RSA) : Cette bibliothèque nous permet de gérer les clés publiques et privées ainsi que le chiffrement/déchiffrement des messages de manière sécurisée.

Flask-Session : Nous avons utilisé cette extension pour gérer les sessions utilisateurs côté serveur, garantissant ainsi que les données de session ne sont pas stockées sur le client.

bcrypt : Ce module permet de hacher et de saler les mots de passe de manière sécurisée, ce qui est essentiel pour la protection des informations d'identification des utilisateurs.

MySQL : Nous avons choisi MySQL pour sa robustesse et sa scalabilité en tant que base de données relationnelle pour stocker les informations des utilisateurs et les messages.

HTML/CSS : La partie front-end utilise HTML pour la structure et CSS pour le style. Flask génère dynamiquement les pages HTML via ses templates.

## Conclusion
Ce projet permet de mettre en place une messagerie sécurisée avec un chiffrement de bout en bout et une gestion sécurisée des utilisateurs et de leurs sessions. L'application est simple, mais elle intègre des pratiques de sécurité avancées pour protéger les données des utilisateurs. La fonctionnalité supplémentaire de recherche d'amis via le username permet d'étendre les capacités sociales de l'application, tout en maintenant un haut niveau de sécurité dans les échanges.

Mise en place du projet
Installation des dépendances : Suivre les étapes ci-dessus pour installer les dépendances nécessaires et configurer l'environnement.

Exécution du projet : Utiliser python run.py pour démarrer l'application une fois la configuration terminée.
