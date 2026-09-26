from flask import render_template, request, redirect
from models.Nutritionist import Nutritionist
from utils import db, app
from flask import Blueprint
import os

bp_nutritionist = Blueprint('nutritionist', __name__, template_folder='templates')

# =-=-=NUTRICIONIST=-=-=
@bp_nutritionist.route('/add', methods=['POST'])
def add_nutritionist():
    file = request.files.get('foto_perfil')
    file.filename = request.form['crn']
    
    if file:
        caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(caminho_completo)
        caminho_banco = caminho_completo

    nutritionist = Nutritionist(
        name = request.form['name'],
        email = request.form['email'],
        crn = request.form['crn'],
        specialization = request.form['especializacao'],
        experience_years = request.form['anos_experiencia'],
        foto_perfil = caminho_banco
    )

    db.session.add(nutritionist)
    db.session.commit()

    return 'Nutricionista adicionado com sucesso!'


@bp_nutritionist.route('/nutritionists')
def get_nutritionists():
    nutritionists = Nutritionist.query.all()

    return (nutritionists)


@bp_nutritionist.route('/<int:id_nutritionist>/update', methods=['POST'])
def update_nutritionist(id_nutritionist):
    nutritionist = Nutritionist.query.get_or_404(id_nutritionist)

    nutritionist.id_user = request.form['id_user']
    nutritionist.name = request.form['name']
    nutritionist.email = request.form['email']
    nutritionist.password = request.form['password']
    nutritionist.crn = request.form['crn']
    nutritionist.specialization = request.form['specialization']
    nutritionist.contributions = request.form['contributions']
    nutritionist.experience = request.form['experience']

    db.session.commit()

    return 'Nutricionista atualizado com sucesso!'


@bp_nutritionist.route('/<int:id_nutritionist>/delete', methods=['POST'])
def delete_nutritionist(id_nutritionist):
    nutritionist = Nutritionist.query.get_or_404(id_nutritionist)

    db.session.delete(nutritionist)
    db.session.commit()

    return 'Nutricionista excluído com sucesso!'