from flask import render_template, request, redirect, url_for, flash
from models.Restriction import Restriction
from utils import db
from flask import Blueprint

bp_restriction = Blueprint('restriction', __name__, template_folder='templates')

# =-=-=RESTRICTION=-=-=
@bp_restriction.route('/add', methods=['POST', 'GET'])
def add_restriction():
    if request.method == 'GET':
        return render_template('restricoes_add.html')
    elif request.method == 'POST':

        new_restriction = Restriction(
            name = request.form['name']
        )
        db.session.add(new_restriction)
        db.session.commit()

        flash('Restrição cadastrada com sucesso!', 'success')
        return redirect(url_for('restriction.get_restrictions'))


@bp_restriction.route('/get', methods=['GET'])
def get_restrictions():
    restrictions = Restriction.query.all()
    len_restrictions = len(restrictions)

    print(restrictions)
    return render_template('restricoes_get.html', restrictions=restrictions, len_restrictions=len_restrictions)


@bp_restriction.route('/<int:id_restriction>/update', methods=['POST', 'GET'])
def update_restriction(id_restriction):
    restriction = Restriction.query.get_or_404(id_restriction)
    if request.method == 'GET':
        return render_template('restricoes_update.html', restriction=restriction)
    elif request.method == 'POST':
        restriction.name = request.form['name']
        db.session.commit()

        return redirect(url_for('restriction.get_restrictions'))


@bp_restriction.route('/<int:id_restriction>/delete')
def delete_restriction(id_restriction):
    restriction = Restriction.query.get_or_404(id_restriction)

    db.session.delete(restriction)
    db.session.commit()

    flash('Restrição excluída com sucesso!', 'success')
    return redirect(url_for('restriction.get_restrictions'))
