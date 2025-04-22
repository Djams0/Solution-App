from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'secure_messaging')

mysql = MySQL(app)
app.config['SESSION_TYPE'] = 'filesystem' 
Session(app)

socketio = SocketIO()
mysql = MySQL()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    mysql.init_app(app)
    socketio.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app



