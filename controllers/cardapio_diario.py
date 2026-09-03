from flask import render_template, request, redirect
from models.Daily_Menu import DailyMenu
from utils import db
from flask import Blueprint

bp_dailyMenu = Blueprint('dailyMenu', __name__, template_folder='templates')

# =-=-=DAILYMENU=-=-=
@bp_dailyMenu.route('/add', methods=['POST'])
def add_daily_menu():
    daily_menu = Daily_Menu(
        id_user = request.form['id_user'],
        day = request.form['day']
    )

    db.session.add(daily_menu)
    db.session.commit()

    return 'Cardápio diário adicionado com sucesso!'


@bp_dailyMenu.route('/daily_menus')
def get_daily_menus():
    daily_menus = Daily_Menu.query.all()

    return str(daily_menus)


@bp_dailyMenu.route('/<int:id_dailyMenu>/update', methods=['POST'])
def update_daily_menu(id_dailyMenu):
    daily_menu = Daily_Menu.query.get_or_404(id_dailyMenu)

    daily_menu.id_user = request.form['id_user']
    daily_menu.day = request.form['day']

    db.session.commit()

    return 'Cardápio diário atualizado com sucesso!'


@bp_dailyMenu.route('/<int:id_dailyMenu>/delete', methods=['POST'])
def delete_daily_menu(id_dailyMenu):
    daily_menu = Daily_Menu.query.get_or_404(id_dailyMenu)

    db.session.delete(daily_menu)
    db.session.commit()

    return 'Cardápio diário excluído com sucesso!'
