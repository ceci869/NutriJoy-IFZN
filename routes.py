from utils import app, admin_required, db
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
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
@login_required
def admin_usuarios():
    if current_user.role != "admin":
        flash("Acesso não permitido", "error")
        return redirect('/homepage')
    usuarios = User.query.filter(User.role != 'admin').all()

    return render_template(
        'admin/usuarios.html',
        usuarios=usuarios
    )


@app.route('/admin/usuarios/novo', methods=['GET', 'POST'])
@login_required
def admin_novo_usuario():
    if current_user.role != "admin":
        flash("Acesso não permitido", "error")
        return redirect('/homepage')
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
@login_required
def admin_editar_usuario(id):
    if current_user.role != "admin":
        flash("Acesso não permitido", "error")
        return redirect('/homepage')
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
@login_required
def admin_excluir_usuario(id):
    if current_user.role != "admin":
        flash("Acesso não permitido", "error")
        return redirect('/homepage')
    usuario = User.query.get_or_404(id)

    if usuario.role == 'admin':
        flash('Não é permitido excluir o administrador por essa página.', 'warning')
        return redirect(url_for('admin_usuarios'))

    db.session.delete(usuario)
    db.session.commit()

    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('admin_usuarios'))

# Lista administrativa
@app.route('/admin/nutricionistas')
@login_required
def admin_nutricionistas():
    if current_user.role != "admin":
        flash("Acesso não permitido", "error")
        return redirect('/homepage')
    nutricionistas = Nutritionist.query.all()

    return render_template(
        'admin/nutricionistas.html',
        nutricionistas=nutricionistas
    )


# Cadastro administrativo
@app.route('/admin/nutricionistas/novo', methods=['GET', 'POST'])
@login_required
def admin_novo_nutricionista():
    if current_user.role != "admin":
        flash("Acesso não permitido", "error")
        return redirect('/homepage')
    if request.method == 'POST':
        crn = request.form.get('crn', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        specialization = request.form.get('specialization', '').strip()
        experience_years = request.form.get('experience_years', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        university = request.form.get('university', '').strip()
        description = request.form.get('description', '').strip()
        file = request.files.get('profile_photo')

        if not all([
            crn, name, email, experience_years,
            city, state, university, description
        ]):
            flash('Preencha todos os campos obrigatórios.', 'warning')
            return redirect(url_for('nutritionist.admin_novo_nutricionista'))

        if Nutritionist.query.filter_by(crn=crn).first():
            flash('Esse CRN já está cadastrado.', 'warning')
            return redirect(url_for('nutritionist.admin_novo_nutricionista'))

        if not file or not file.filename:
            flash('Envie uma foto de perfil.', 'warning')
            return redirect(url_for('nutritionist.admin_novo_nutricionista'))

        filename = secure_filename(crn + '_' + file.filename)
        caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(caminho_completo)

        nutricionista = Nutritionist(
            crn=int(crn),
            name=name,
            email=email,
            specialization=specialization,
            experience_years=int(experience_years),
            profile_photo=caminho_completo,
            city=city,
            state=state,
            university=university,
            description=description
        )

        db.session.add(nutricionista)
        db.session.commit()

        flash('Nutricionista cadastrado com sucesso!', 'success')
        return redirect(url_for('nutritionist.admin_nutricionistas'))

    return render_template('admin/novo_nutricionista.html')


# Edição administrativa
@app.route(
    '/admin/nutricionistas/<int:crn>/editar',
    methods=['GET', 'POST']
)
@login_required
def admin_editar_nutricionista(crn):
    if current_user.role != "admin":
        flash("Acesso não permitido", "error")
        return redirect('/homepage')
    nutricionista = Nutritionist.query.get_or_404(crn)

    if request.method == 'POST':
        nutricionista.name = request.form.get('name', '').strip()
        nutricionista.email = request.form.get('email', '').strip()
        nutricionista.specialization = request.form.get('specialization', '').strip()
        nutricionista.experience_years = int(
            request.form.get('experience_years', 0)
        )
        nutricionista.city = request.form.get('city', '').strip()
        nutricionista.state = request.form.get('state', '').strip()
        nutricionista.university = request.form.get('university', '').strip()
        nutricionista.description = request.form.get('description', '').strip()

        file = request.files.get('profile_photo')

        if file and file.filename:
            filename = secure_filename(str(crn) + '_' + file.filename)
            caminho_completo = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
            file.save(caminho_completo)
            nutricionista.profile_photo = caminho_completo

        db.session.commit()

        flash('Nutricionista atualizado com sucesso!', 'success')
        return redirect(url_for('nutritionist.admin_nutricionistas'))

    return render_template(
        'admin/editar_nutricionista.html',
        nutricionista=nutricionista
    )


# Exclusão administrativa
@app.route(
    '/admin/nutricionistas/<int:crn>/excluir',
    methods=['POST']
)
@login_required
def admin_excluir_nutricionista(crn):
    if current_user.role != "admin":
        flash("Acesso não permitido", "error")
        return redirect('/homepage')
    nutricionista = Nutritionist.query.get_or_404(crn)

    db.session.delete(nutricionista)
    db.session.commit()

    flash('Nutricionista excluído com sucesso!', 'success')
    return redirect(url_for('nutritionist.admin_nutricionistas'))