from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from models.User import User
from models.Restriction import Restriction
from utils import db
from flask import Blueprint
from app import lm
import hashlib


@lm.user_loader
def user_loader(id):
    return db.session.query(User).filter_by(id=id).first()


def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()


bp_user = Blueprint('user', __name__, template_folder='templates')


# =-=-= CADASTRO DE USUÁRIO =-=-=
@bp_user.route('/add', methods=['GET', 'POST'])
def add_user():
    allrestrictions = Restriction.query.all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        restrictions_ids = request.form.getlist('restricoes')

        if name and email and password:
            new_user = User(
                name=name,
                email=email,
                password=hash(password)
            )

            if restrictions_ids:
                selected_restrictions = Restriction.query.filter(
                    Restriction.id.in_(restrictions_ids)
                ).all()

                new_user.restrictions.extend(selected_restrictions)

            db.session.add(new_user)
            db.session.commit()

            flash('Usuário cadastrado com sucesso!', 'success')
            login_user(new_user)

            return redirect(url_for('homepage'))

        flash('Por favor preencha os campos obrigatórios', 'warning')
        return redirect(url_for('user.add_user'))

    return render_template('cadastro.html', allrestrictions=allrestrictions)


# =-=-= LOGIN =-=-=
@bp_user.route('/verificalogin', methods=['GET', 'POST'])
def verificalogin():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not email or not password:
        flash('Preencha o email e a senha.', 'warning')
        return redirect(url_for('user.verificalogin'))

    user = User.query.filter_by(
        email=email,
        password=hash(password)
    ).first()

    if user is None:
        flash('Email ou senha incorretos. Tente novamente.', 'error')
        return redirect(url_for('user.verificalogin'))

    login_user(user)

    flash('Usuário logado com sucesso!', 'success')

    return redirect(url_for('homepage'))


# =-=-= LOGOUT =-=-=
@bp_user.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.verificalogin'))


# =-=-= LISTAR USUÁRIOS =-=-=
@bp_user.route('/users')
def get_users():
    users = User.query.all()
    return str(users)


# =-=-= ATUALIZAR USUÁRIO =-=-=
@bp_user.route('/<int:id_user>/update', methods=['POST'])
@login_required
def update_user(id_user):
    user = User.query.get_or_404(id_user)

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if name:
        user.name = name

    if email:
        user.email = email

    if password:
        user.password = hash(password)

    db.session.commit()

    return 'Usuário atualizado com sucesso!'


# =-=-= EXCLUIR USUÁRIO =-=-=
@bp_user.route('/<int:id_user>/delete', methods=['POST'])
@login_required
def delete_user(id_user):
    user = User.query.get_or_404(id_user)

    if user.id == int(current_user.get_id()):
        flash('Você não pode excluir sua própria conta enquanto estiver logado.', 'warning')
        return redirect(url_for('homepage'))

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('index'))