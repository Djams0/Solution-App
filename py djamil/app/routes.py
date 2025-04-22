from flask import Blueprint, render_template
from flask import request, redirect, render_template, flash, url_for, session
from app.services.authentification import register_user, authenticate_user
from app.services.home import get_user_friends
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from app.services.authentification import authenticate_user
from app.services.chat import send_message, get_messages


main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' in session:
        friends = get_user_friends(session['user_id'])
        return render_template('index.html', username=session['username'], friends=friends)
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