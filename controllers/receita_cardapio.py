from flask import render_template, request, redirect
from models.Menu_Recipe import MenuRecipe
from utils import db
from flask import Blueprint

bp_menuRecipe = Blueprint('menu_recipe', __name__, template_folder='templates')

# =-=-=MENURECIPE=-=-=
@bp_menuRecipe.route('/add', methods=['POST'])
def add_menu_recipe():
    menu_recipe = Menu_Recipe(
        id_dailyMenu=request.form['id_dailyMenu'],
        id_recipe=request.form['id_recipe']
    )

    db.session.add(menu_recipe)
    db.session.commit()

    return 'Receita adicionada ao cardápio com sucesso!'


@bp_menuRecipe.route('/menu_recipes')
def get_menu_recipes():
    menu_recipes = Menu_Recipe.query.all()

    return str(menu_recipes)


@bp_menuRecipe.route('/<int:id_dailyMenu>/<int:id_recipe>/update',
           methods=['POST'])
def update_menu_recipe(id_dailyMenu, id_recipe):
    menu_recipe = Menu_Recipe.query.filter_by(
        id_dailyMenu=id_dailyMenu,
        id_recipe=id_recipe
    ).first_or_404()

    menu_recipe.id_dailyMenu = request.form['id_dailyMenu']
    menu_recipe.id_recipe = request.form['id_recipe']

    db.session.commit()

    return 'Receita do cardápio atualizada com sucesso!'


@bp_menuRecipe.route('/<int:id_dailyMenu>/<int:id_recipe>/delete',
           methods=['POST'])
def delete_menu_recipe(id_dailyMenu, id_recipe):
    menu_recipe = Menu_Recipe.query.filter_by(
        id_dailyMenu = id_dailyMenu,
        id_recipe = id_recipe
    ).first_or_404()

    db.session.delete(menu_recipe)
    db.session.commit()

    return 'Receita removida do cardápio com sucesso!'
