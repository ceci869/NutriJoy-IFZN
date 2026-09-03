from flask import render_template, request, redirect
from models.Recipe import Recipe
from utils import db
from flask import Blueprint

bp_recipe = Blueprint('recipe', __name__, template_folder='templates')

# =-=-=RECIPE=-=-=
@bp_recipe.route('/add', methods=['POST'])
def add_recipe():
    recipe = Recipe(
        id_nutritionist = request.form['id_nutritionist'],
        name = request.form['name'],
        average_value = request.form['average_value'],
        kcal = request.form['kcal'],
        fats = request.form['fats'],
        carbohydrates = request.form['carbohydrates'],
        fibers = request.form['fibers'],
        proteins = request.form['proteins']
    )

    db.session.add(recipe)
    db.session.commit()

    return 'Receita adicionada com sucesso!'


@bp_recipe.route('/recipes')
def get_recipes():
    recipes = Recipe.query.all()

    return str(recipes)


@bp_recipe.route('/<int:id_recipe>/update', methods=['POST'])
def update_recipe(id_recipe):
    recipe = Recipe.query.get_or_404(id_recipe)

    recipe.id_nutritionist = request.form['id_nutritionist']
    recipe.name = request.form['name']
    recipe.average_value = request.form['average_value']
    recipe.kcal = request.form['kcal']
    recipe.fats = request.form['fats']
    recipe.carbohydrates = request.form['carbohydrates']
    recipe.fibers = request.form['fibers']
    recipe.proteins = request.form['proteins']

    db.session.commit()

    return 'Receita atualizada com sucesso!'


@bp_recipe.route('/<int:id_recipe>/delete', methods=['POST'])
def delete_recipe(id_recipe):
    recipe = Recipe.query.get_or_404(id_recipe)

    db.session.delete(recipe)
    db.session.commit()

    return 'Receita excluída com sucesso!'