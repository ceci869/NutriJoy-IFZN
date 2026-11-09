from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from models.User import User
from models.Nutritionist import Nutritionist
from models.Restriction import Restriction
from utils import db, app
from flask import Blueprint
from app import lm
import hashlib
from flask import flash


@lm.user_loader
def user_loader(id):
    return db.session.query(User).filter_by(id=id).first()


def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()


bp_user = Blueprint('user', __name__, template_folder='templates')

bp_admin = Blueprint('admin', __name__, template_folder='templates/admin')


# =-=-= CADASTRO DE USUÁRIO =-=-=
@bp_user.route('/add', methods=['GET', 'POST'])
def add_user():
    allrestrictions = Restriction.query.all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        cep = request.form.get('cep', '').strip()
        age = request.form.get('age', '').strip()
        restrictions_ids = request.form.getlist('restricoes')

        if name and email and password:
            new_user = User(
                name=name,
                email=email,
                password=hash(password),
                cep=cep,
                age=age
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


# =-=-= ATUALIZAR USUÁRIO =-=-=
@bp_user.route('/<int:id_user>/update', methods=['POST'])
@login_required
def update_user(id_user):
    user = User.query.get_or_404(id_user)
    
    name = request.form['name'].strip()
    email = request.form['email'].strip()
    # password = request.form['password'].strip()
    restrictions = request.form.getlist('restricao') 

    if not name and not email and not restrictions:
        flash("Não é possível realizar a atualização!", "error")
        return redirect("/gerenciarperfil")

    if name:
        user.name = name

    if email:
        user.email = email

    db.session.commit()
    flash("Usuário atualizado com sucesso!", "success")
    return redirect("/gerenciarperfil")


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

    flash('Perfil excluído com sucesso', 'success')
    return redirect(url_for('index'))


# =-=-=- ADMINISTRAÇÃO -=-=-=
@bp_admin.route('/usuarios')
@login_required
def admin_usuarios():
    if current_user.role != "admin":
        flash("Acesso não permitido", "error")
        return redirect('/homepage')
    usuarios = User.query.filter(User.role != 'admin').all()

    return render_template('admin/usuarios.html', usuarios=usuarios)


@bp_admin.route('/usuarios/novo', methods=['GET', 'POST'])
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
            password=hash(password)
        )
        usuario.role = 'usuario'

        db.session.add(usuario)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('admin_usuarios'))

    return render_template('admin/novo_usuario.html')


@bp_admin.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
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


@bp_admin.route('/usuarios/<int:id>/excluir', methods=['POST'])
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
@bp_admin.route('/nutricionistas')
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
@bp_admin.route('/nutricionistas/novo', methods=['GET', 'POST'])
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
@bp_admin.route(
    '/nutricionistas/<int:crn>/editar',
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
@bp_admin.route(
    '/nutricionistas/<int:crn>/excluir',
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