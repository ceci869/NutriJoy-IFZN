from flask import render_template, request, redirect
from models.Nutritionist import Nutritionist
from utils import db
from flask import Blueprint

bp_nutritionist = Blueprint('nutritionist', __name__, template_folder='templates')

# =-=-=NUTRICIONIST=-=-=
@bp_nutritionist.route('/add', methods=['POST'])
def add_nutritionist():
    nutritionist = Nutritionist(
        id_user = request.form['id_user'],
        name = request.form['name'],
        email = request.form['email'],
        password = request.form['password'],
        crn = request.form['crn'],
        specialization = request.form['specialization'],
        contributions = request.form['contributions'],
        experience = request.form['experience']
    )

    db.session.add(nutritionist)
    db.session.commit()

    return 'Nutricionista adicionado com sucesso!'


@bp_nutritionist.route('/nutritionists')
def get_nutritionists():
    nutritionists = Nutritionist.query.all()

    return str(nutritionists)


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