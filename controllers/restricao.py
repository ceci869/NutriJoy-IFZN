from flask import render_template, request, redirect
from models.Restriction import Restriction
from utils import db
from flask import Blueprint

bp_restriction = Blueprint('restriction', __name__, template_folder='templates')

# =-=-=RESTRICTION=-=-=
@bp_restriction.route('/add', methods=['POST'])
def add_restriction():
    restriction = Restriction(
        name = request.form['alergia_intolerancia']
    )

    db.session.add(restriction)
    db.session.commit()

    return 'Restrição adicionada com sucesso!'


@bp_restriction.route('/restrictions')
def get_restrictions():
    restrictions = Restriction.query.all()

    return str(restrictions)


@bp_restriction.route('/<int:id_restriction>/update', methods=['POST'])
def update_restriction(id_restriction):
    restriction = Restriction.query.get_or_404(id_restriction)

    restriction.name = request.form['name']

    db.session.commit()

    return 'Restrição atualizada com sucesso!'


@bp_restriction.route('/<int:id_restriction>/delete', methods=['POST'])
def delete_restriction(id_restriction):
    restriction = Restriction.query.get_or_404(id_restriction)

    db.session.delete(restriction)
    db.session.commit()

    return 'Restrição excluída com sucesso!'
