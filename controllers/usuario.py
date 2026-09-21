from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from models.User import User
from utils import db
from flask import Blueprint
from app import lm
import hashlib

@lm.user_loader
def user_loader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()

bp_user = Blueprint('user', __name__, template_folder='templates')

# =-=-=USER=-=-=
@bp_user.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('cadastro.html')
    elif request.method == 'POST':
        
        name = request.form['name'],
        email = request.form['email'],
        password = request.form['password']
        
        new_user = User(name=name, email=email, password=hash(password))

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('homepage'))

@bp_user.route('/verificalogin', methods=['POST'])
def verificalogin():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = db.session.query(User).filter_by(email=email, password=hash(password)).first()
        if not user:
            return 'Nome ou senha incorretos'
        
        login_user(user)
        return redirect(url_for('homepage'))

@bp_user.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@bp_user.route('/users')
def get_users():
    users = User.query.all()

    return str(users)


@bp_user.route('/<int:id_user>/update', methods=['POST'])
@login_required
def update_user(id_user):
    user = User.query.get_or_404(id_user)
    
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    password=hash(password)

    if name:
        user.name = name

    if email:
        user.email = email

    if password:
        user.password = password

    db.session.commit()

    return 'Usuário atualizado com sucesso!'


@bp_user.route('/<int:id_user>/delete', methods=['POST'])
@login_required
def delete_user(id_user):
    user = User.query.get_or_404(id_user)

    db.session.delete(user)
    db.session.commit()

    return 'Usuário excluído com sucesso!'