from flask import render_template, request, redirect
from models.User_Restriction import UserRestriction
from utils import db
from flask import Blueprint

bp_userRestriction = Blueprint('user_restriction', __name__, template_folder='templates')

# =-=-=USERRESTRICTION=-=-=
@bp_userRestriction.route('/add', methods=['POST'])
def add_user_restriction():
    user_restriction = User_Restriction(
        id_user = request.form['id_user'],
        id_restriction = request.form['id_restriction'],
        name = request.form['name']
    )

    db.session.add(user_restriction)
    db.session.commit()

    return 'Restrição do usuário adicionada com sucesso!'


@bp_userRestriction.route('/user_restriction')
def get_user_restrictions():
    user_restrictions = User_Restriction.query.all()

    return str(user_restrictions)


@bp_userRestriction.route('/<int:id_user>/<int:id_restriction>/update',
           methods=['POST'])
def update_user_restriction(id_user, id_restriction):
    user_restriction = User_Restriction.query.filter_by(
        id_user = id_user,
        id_restriction = id_restriction
    ).first_or_404()

    user_restriction.name = request.form['name']

    db.session.commit()

    return 'Restrição do usuário atualizada com sucesso!'


@bp_userRestriction.route('/<int:id_user>/<int:id_restriction>/delete',
           methods=['POST'])
def delete_user_restriction(id_user, id_restriction):
    user_restriction = User_Restriction.query.filter_by(
        id_user = id_user,
        id_restriction = id_restriction
    ).first_or_404()

    db.session.delete(user_restriction)
    db.session.commit()

    return 'Restrição do usuário excluída com sucesso!'