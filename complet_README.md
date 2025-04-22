# Messagerie Sécurisée avec Chiffrement de Bout en Bout

## 1. Introduction
Ce projet vise à développer une application de messagerie sécurisée en Python, en utilisant Flask pour le backend, MySQL pour la gestion de la base de données, et HTML/CSS pour la création d'une interface utilisateur web. L'application met en œuvre un chiffrement de bout en bout basé sur des clés RSA pour garantir que seules les personnes autorisées puissent lire les messages.

### 1.1 Technologies utilisées
- **Python** : Langage de programmation principal du projet.
- **Flask** : Framework web léger pour gérer les routes, les sessions, et les requêtes HTTP.
- **MySQL** : Base de données pour stocker les informations des utilisateurs, les messages chiffrés, et les clés publiques.
- **HTML / CSS** : Technologies pour la création de l'interface web.
- **cryptography** : Bibliothèque pour la gestion du chiffrement (RSA) et du hachage (bcrypt) des mots de passe.
- **bcrypt** : Bibliothèque pour le hachage sécurisé des mots de passe.
- **Flask-Session** : Pour gérer les sessions utilisateur de manière sécurisée.
- **dotenv** : Pour charger les variables d'environnement depuis un fichier `.env`.

## 2. Architecture du Projet

Voici l'architecture du projet et les principales structures de fichiers :

