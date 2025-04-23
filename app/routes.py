from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from app.services.chat import ChatService
from app.services.user import User
from app import mysql

main = Blueprint('main', __name__)

user_manager = User(mysql)
chat_service = ChatService(mysql, session)

@main.route('/')
def index():
    if 'user_id' in session:
        friends = user_manager.get_friends(session['user_id'])
        return render_template('index.html', username=session['username'], friends=friends)
    else:
        return redirect(url_for('main.login'))

@main.route('/mes_reseaux')
def mes_reseaux():
    if 'user_id' in session:
        user_id = session['user_id']
        pending_requests = user_manager.get_pending_requests(user_id)
        return render_template(
            'mes_reseaux.html',
            username=session['username'],
            demandes_envoyees=pending_requests['envoyees'],
            demandes_recues=pending_requests['recues']
        )
    else:
        return redirect(url_for('main.login'))

@main.route('/update_request/<int:user_id_to>/<string:action>', methods=['POST'])
def update_request(user_id_to, action):
    if 'user_id' in session:
        user_id = session['user_id']
        user_manager.update_friend_status(user_id, user_id_to, action)
        return redirect(url_for('main.mes_reseaux'))
    else:
        return redirect(url_for('main.login'))

@main.route('/chat/<int:ami_id>', methods=['GET', 'POST'])
def chat(ami_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        message = request.form['message']
        success, info = chat_service.send_message(ami_id, message)
        if not success:
            flash(info, 'danger')

    messages = chat_service.get_messages(ami_id)
    return render_template('chat.html', messages=messages, ami_id=ami_id)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_manager.login(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Connexion réussie !', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.', 'danger')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message = user_manager.register(username, password)
        if success:
            flash(message, 'success')
            return redirect(url_for('main.index'))
        else:
            flash(message, 'danger')
    return render_template('register.html')

@main.route('/logout')
def logout():
    session.clear()
    flash("Vous êtes déconnecté.", 'info')
    return redirect(url_for('main.login'))

@main.route('/recherche', methods=['GET', 'POST'])
def recherche():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        username = request.form.get('username')
        users = user_manager.search_users(username)
        return render_template('recherche.html', users=users, username=session['username'])
    return render_template('recherche.html', username=session['username'])

@main.route('/send_friend_request/<int:user_id_to>', methods=['POST'])
def send_request(user_id_to):
    if 'user_id' in session:
        user_id_from = session['user_id']
        user_manager.send_friend_request(user_id_from, user_id_to)
        return redirect(url_for('main.recherche'))
    else:
        return redirect(url_for('main.login'))
