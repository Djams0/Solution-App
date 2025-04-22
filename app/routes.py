from flask import Blueprint, render_template
from flask import request, redirect, render_template, flash, url_for, session
from app.services.authentification import register_user, authenticate_user
from app.services.home import get_user_friends
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from app.services.authentification import authenticate_user
from app.services.chat import send_message, get_messages
from app.services.mes_reseaux import get_pending_requests, update_friend_request_status
from app.services.recherche import search_user, send_friend_request


main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' in session:
        friends = get_user_friends(session['user_id'])
        return render_template('index.html', username=session['username'], friends=friends)
    else:
        return redirect(url_for('main.login'))
    
@main.route('/mes_reseaux')
def mes_reseaux():
    if 'user_id' in session:
        user_id = session['user_id']
        pending_requests = get_pending_requests(user_id)
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
        # Appelle la fonction pour mettre à jour le statut de la demande
        update_friend_request_status(user_id, user_id_to, action)
        return redirect(url_for('main.mes_reseaux'))
    else:
        return redirect(url_for('main.login'))
    
    
@main.route('/chat/<int:ami_id>', methods=['GET', 'POST'])
def chat(ami_id):
    if request.method == 'POST':
        message = request.form['message']
        success, info = send_message(ami_id, message)
        if not success:
            flash(info, 'danger')

    messages = get_messages(ami_id)
    return render_template('chat.html', messages=messages, ami_id=ami_id)

    

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
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
        success, message = register_user(username, password)
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
    if 'user_id' in session:
        if request.method == 'POST':
            username = request.form.get('username')
            users = search_user(username)
            return render_template('recherche.html', users=users, username=session['username'])
        return render_template('recherche.html', username=session['username'])
    else:
        return redirect(url_for('main.login'))

@main.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    if 'user_id' not in session:
        flash("Vous devez être connecté pour envoyer une demande d'amitié.", 'warning')
        return redirect(url_for('main.login'))

    friend_id = request.form.get('friend_id')
    user_id = session['user_id']

    if not friend_id:
        flash("Identifiant de l'utilisateur manquant.", 'danger')
        return redirect(url_for('main.reseau'))

    success, message = send_friend_request(user_id, friend_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('main.reseau'))