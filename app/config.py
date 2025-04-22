import os

class Config:

    MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
    MYSQL_USER = os.getenv('DB_USER', 'root')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD', '')
    MYSQL_DB = os.getenv('DB_NAME', 'secure_messaging')
    SECRET_KEY = os.getenv('SECRET_KEY', '12345678')
