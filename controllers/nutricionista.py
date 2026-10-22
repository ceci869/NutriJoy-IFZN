from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models.Nutritionist import Nutritionist
from utils import db, app, admin_required
import os

bp_nutritionist = Blueprint(
    'nutritionist',
    __name__,
    template_folder='templates'
)


# Cadastro público existente
@bp_nutritionist.route('/add', methods=['POST'])
def add_nutritionist():
    file = request.files.get('profile_photo')

    if not file or not file.filename:
        return 'Envie uma foto de perfil.', 400

    crn = request.form.get('crn', '').strip()

    if not crn:
        return 'Informe o CRN.', 400

    filename = secure_filename(crn + '_' + file.filename)
    caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(caminho_completo)

    nutritionist = Nutritionist(
        crn=int(crn),
        name=request.form['name'],
        email=request.form['email'],
        specialization=request.form.get('especializacao'),
        experience_years=int(request.form['anos_experiencia']),
        profile_photo=caminho_completo,
        city=request.form['city'],
        state=request.form['state'],
        university=request.form['university'],
        description=request.form['description']
    )

    db.session.add(nutritionist)
    db.session.commit()

    return 'Nutricionista adicionado com sucesso!'


def get_nutritionists():
    return Nutritionist.query.all()


# Lista administrativa
@bp_nutritionist.route('/admin/nutricionistas')
@admin_required
def admin_nutricionistas():
    nutricionistas = Nutritionist.query.all()

    return render_template(
        'admin/nutricionistas.html',
        nutricionistas=nutricionistas
    )


# Cadastro administrativo
@bp_nutritionist.route('/admin/nutricionistas/novo', methods=['GET', 'POST'])
@admin_required
def admin_novo_nutricionista():
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
@bp_nutritionist.route(
    '/admin/nutricionistas/<int:crn>/editar',
    methods=['GET', 'POST']
)
@admin_required
def admin_editar_nutricionista(crn):
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
@bp_nutritionist.route(
    '/admin/nutricionistas/<int:crn>/excluir',
    methods=['POST']
)
@admin_required
def admin_excluir_nutricionista(crn):
    nutricionista = Nutritionist.query.get_or_404(crn)

    db.session.delete(nutricionista)
    db.session.commit()

    flash('Nutricionista excluído com sucesso!', 'success')
    return redirect(url_for('nutritionist.admin_nutricionistas'))