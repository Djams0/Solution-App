# Messagerie Sécurisée avec Chiffrement de Bout en Bout

## Description

Ce projet développe une application de messagerie sécurisée en **Python** en utilisant **Flask** pour le backend, **MySQL** pour la gestion de la base de données, et **HTML/CSS** pour la création de l'interface utilisateur web. L'application met en œuvre un **chiffrement de bout en bout** basé sur des clés **RSA** pour garantir que seules les personnes autorisées puissent lire les messages.

## Fonctionnalités

- **Chiffrement de bout en bout** des messages avec **RSA** : Seuls l'expéditeur et le destinataire peuvent lire les messages échangés.
- **Hachage et salage des mots de passe** pour assurer la sécurité des informations d'identification des utilisateurs.
- **Gestion des sessions** avec **Flask-Session** pour authentifier et suivre les utilisateurs de manière sécurisée.
- **Interface utilisateur** moderne en **HTML** et **CSS**, hébergée sur un serveur **Flask**.
- **Base de données MySQL** pour stocker les informations des utilisateurs, messages et clés publiques.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- **Python 3.x** installé sur votre machine.
- **MySQL** installé et configuré.
- Un éditeur de texte comme **VSCode** ou **PyCharm**.

## Installation

### 1. Cloner le projet

Clonez le projet en utilisant Git :

git clone <url-du-repository>


### 2. Créer un environnement virtuel

Créez un environnement virtuel pour éviter les conflits avec les packages système :

python3 -m venv venv


### 3. Activer l'environnement virtuel

- **Sur Windows** :

venv\Scripts\activate


- **Sur Linux/Mac** :

source venv/bin/activate


### 4. Installer les dépendances

Installez les dépendances nécessaires :

pip install -r requirements.txt


Le fichier `requirements.txt` contient les dépendances suivantes :

- **Flask==2.1.1**
- **cryptography==3.4.8**
- **flask-session==0.4.0**
- **mysql-connector-python==8.0.27**
- **bcrypt==3.2.0**
- **python-dotenv==0.19.0**

### 5. Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet et ajoutez-y les variables suivantes (exemple) :

FLASK_APP=run.py FLASK_ENV=development SECRET_KEY=your_secret_key DB_HOST=localhost DB_USER=root DB_PASSWORD=your_password DB_NAME=messaging_db


### 6. Créer la base de données

Créez une base de données **MySQL** pour stocker les informations de l'application.

### 7. Démarrer l'application

Une fois les dépendances installées et la base de données configurée, vous pouvez démarrer l'application en exécutant :

python run.py

rust
Copier
Modifier

L'application sera accessible à l'adresse : `http://127.0.0.1:5000`.

## Architecture du Projet

Voici l'architecture du projet :

app/
│
├── services/                # Services métiers (authentification, chat, réseaux sociaux, recherche)
│   ├── authentification.py  # Gestion de l'authentification et des mots de passe
│   ├── chat.py              # Gestion des messages chiffrés
│   ├── home.py              # Accueil de l'application
│   ├── mes_reseaux.py       # Réseaux sociaux des utilisateurs
│   └── recherche.py         # Fonctionnalités de recherche dans les messages
│
├── static/                  # Fichiers statiques (CSS, JS)
│   ├── css/                 # Styles CSS
│   └── js/                  # Scripts JavaScript
│
├── templates/               # Templates HTML
├── __init__.py              # Initialisation de l'application Flask
├── config.py                # Configuration de l'application
├── routes.py                # Définition des route
├── run.py
└── private_keys/            # Clés privées stockées localement pour chaque utilisateur
│
├── flask_session/           # Gestion des sessions
└── local_storage/           # Stockage local des messages envoyés

## Fichiers principaux

- **app/__init__.py** : Point d'entrée de l'application Flask, initialise les configurations et les extensions comme **Flask-Session**.
- **app/config.py** : Contient la configuration de l'application, comme les informations de la base de données et les clés secrètes.
- **app/routes.py** : Définition des routes HTTP qui gèrent les pages de l'application.
- **run.py** : Le script principal pour démarrer l'application Flask.

## Fonctionnalités

### 1. Chiffrement RSA

L'application utilise l'algorithme **RSA** pour chiffrer les messages envoyés. Lorsqu'un utilisateur envoie un message à un autre, il est chiffré avec la clé publique du destinataire, garantissant ainsi que seul ce dernier pourra le déchiffrer avec sa clé privée.

### 2. Hachage et Salage des mots de passe

Les mots de passe des utilisateurs sont hachés et salés avant d'être stockés en base de données. Le processus utilise **bcrypt**, qui ajoute une couche de sécurité pour éviter les attaques par force brute.

### 3. Gestion des sessions avec Flask

Les sessions sont gérées avec **Flask-Session**, ce qui permet de suivre les utilisateurs de manière sécurisée tout au long de leur interaction avec l'application.

## Choix Techniques

### Flask vs Tkinter

Au départ, **Tkinter** a été proposé pour l'interface utilisateur. Cependant, nous avons choisi **Flask** avec une interface web pour plusieurs raisons :

- **Accessibilité** : Flask permet de créer une application web accessible depuis n'importe quel navigateur, tandis que Tkinter restreint l'utilisation à une interface de bureau.
- **Design et Flexibilité** : Flask permet d'utiliser **HTML** et **CSS**, offrant ainsi une plus grande liberté pour la création d'interfaces modernes et réactives.
- **Séparation des préoccupations** : Avec Flask, nous séparons mieux la logique du serveur et l'interface utilisateur, ce qui facilite la maintenance et l'ajout de nouvelles fonctionnalités.

## Conclusion

Ce projet offre une solution de **messagerie sécurisée** avec **chiffrement de bout en bout** et gestion des utilisateurs via une interface web moderne. L'utilisation de **Flask** permet une architecture flexible et évolutive, tout en garantissant la sécurité des communications grâce à des techniques telles que le chiffrement **RSA** et le hachage des mots de passe avec **bcrypt**.
