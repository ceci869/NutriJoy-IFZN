from utils import app, admin_required, db
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from time import sleep
import json

from models.User import User
from models.Daily_Menu import DailyMenu
from models.Recipe import Recipe
from models.Food import Food
from models.Nutritionist import Nutritionist
from models.Restriction import Restriction
# from models.User_Restriction import UserRestriction
from models.Menu_Recipe import MenuRecipe
from models.Food_Recipe import FoodRecipe
from controllers.usuario import bp_user, hash as hash_password
from controllers.alimento import bp_food
from controllers.cardapio_diario import bp_dailyMenu
from controllers.nutricionista import bp_nutritionist, get_nutritionists
from controllers.receita import bp_recipe
from controllers.restricao import bp_restriction
# from controllers.usuario_restricao import bp_userRestriction
from controllers.comida_receita import bp_foodRecipe
from controllers.receita_cardapio import bp_menuRecipe

app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_food, url_prefix='/food')
app.register_blueprint(bp_dailyMenu, url_prefix='/dailyMenu')
app.register_blueprint(bp_nutritionist, url_prefix='/nutritionist')
app.register_blueprint(bp_recipe, url_prefix='/recipe')
app.register_blueprint(bp_restriction, url_prefix='/restriction')
# app.register_blueprint(bp_userRestriction, url_prefix='/user_restriction')
app.register_blueprint(bp_menuRecipe, url_prefix='/menu_recipe')
app.register_blueprint(bp_foodRecipe, url_prefix='/food_recipe')


@app.route('/')
def index():
    lista_colaboradores = [
        'Alba Lopes',
        'Cecília Aine',
        'Maria Luísa',
        'Thaylanne Kérrinna'
    ]
    return render_template('index.html', lista_colaboradores=lista_colaboradores)


@app.route('/paginaerro')
def paginaerro():
    return render_template('paginaerro.html')


@app.route('/homepage')
@login_required
def homepage():
    nutritionists = get_nutritionists()
    return render_template('homepage.html', nutritionists=nutritionists)


@app.route('/catalogodereceitas')
@login_required
def catalogodereceitas():
    lista_receitas = [
        {'nome': 'Sanduíches kawaii',
         'foto': url_for('static', filename='img/receita1.jpg')},
        {'nome': 'Pizza kawaii',
         'foto': url_for('static', filename='img/receita2.jpg')},
        {'nome': 'Curry kawaii',
         'foto': url_for('static', filename='img/receita3.jpg')},
        {'nome': 'Sushi kawaii',
         'foto': url_for('static', filename='img/receita4.jpg')},
        {'nome': 'Pudim kawaii',
         'foto': url_for('static', filename='img/receita5.jpg')}
    ]

    return render_template(
        'catalogo_de_receitas.html',
        lista_receitas=lista_receitas
    )


@app.route('/cardapiosemanal')
@login_required
def cardapiosemanal():
    return render_template('cardapiosemanal.html')


@app.route('/gerenciarperfil', methods=['GET', 'POST'])
@login_required
def gerenciarperfil():
    opcao = 'Nenhum selecionado'
    return render_template('gerenciarperfil.html', opcao=opcao)


@app.route('/perfilnutricionista/<int:nutritionist_crn>')
@login_required
def perfilnutricionista(nutritionist_crn):
    nutritionist = Nutritionist.query.get_or_404(nutritionist_crn)
    return render_template(
        'perfilnutricionista.html',
        nutritionist=nutritionist
    )


@app.route('/formularionutricionista')
def formulario_nutricionista():
    return render_template('formulario_nutricionista.html')


# =-=-=- ADMINISTRAÇÃO -=-=-=
@app.route('/admin/usuarios')
@admin_required
def admin_usuarios():
    usuarios = User.query.filter(User.role != 'admin').all()

    return render_template(
        'admin/usuarios.html',
        usuarios=usuarios
    )


@app.route('/admin/usuarios/novo', methods=['GET', 'POST'])
@admin_required
def admin_novo_usuario():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not name or not email or not password:
            flash('Preencha todos os campos.', 'warning')
            return redirect(url_for('admin_novo_usuario'))

        if User.query.filter_by(email=email).first():
            flash('Esse email já está cadastrado.', 'warning')
            return redirect(url_for('admin_novo_usuario'))

        usuario = User(
            name=name,
            email=email,
            password=hash_password(password)
        )
        usuario.role = 'usuario'

        db.session.add(usuario)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('admin_usuarios'))

    return render_template('admin/novo_usuario.html')


@app.route('/admin/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_usuario(id):
    usuario = User.query.get_or_404(id)

    if usuario.role == 'admin':
        return redirect(url_for('admin_usuarios'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()

        if not name or not email:
            flash('Nome e email são obrigatórios.', 'warning')
            return redirect(url_for('admin_editar_usuario', id=id))

        outro_usuario = User.query.filter_by(email=email).first()

        if outro_usuario and outro_usuario.id != usuario.id:
            flash('Esse email já está cadastrado.', 'warning')
            return redirect(url_for('admin_editar_usuario', id=id))

        usuario.name = name
        usuario.email = email

        db.session.commit()

        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('admin_usuarios'))

    return render_template('admin/editar_usuario.html', usuario=usuario)


@app.route('/admin/usuarios/<int:id>/excluir', methods=['POST'])
@admin_required
def admin_excluir_usuario(id):
    usuario = User.query.get_or_404(id)

    if usuario.role == 'admin':
        flash('Não é permitido excluir o administrador por essa página.', 'warning')
        return redirect(url_for('admin_usuarios'))

    db.session.delete(usuario)
    db.session.commit()

    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('admin_usuarios'))