from flask import render_template, request, redirect
from models.Food_Recipe import FoodRecipe
from utils import db
from flask import Blueprint

bp_foodRecipe = Blueprint('food_recipe', __name__, template_folder='templates')

# =-=-=FOODRECIPE=-=-=
@bp_foodRecipe.route('/add', methods=['POST'])
def add_food_recipe():
    food_recipe = Food_Recipe(
        id_food = request.form['id_food'],
        id_recipe = request.form['id_recipe']
    )

    db.session.add(food_recipe)
    db.session.commit()

    return 'Alimento adicionado à receita com sucesso!'


@bp_foodRecipe.route('/food_recipes')
def get_food_recipes():
    food_recipes = Food_Recipe.query.all()

    return str(food_recipes)


@bp_foodRecipe.route('/<int:id_food>/<int:id_recipe>/update',
           methods=['POST'])
def update_food_recipe(id_food, id_recipe):
    food_recipe = Food_Recipe.query.filter_by(
        id_food = id_food,
        id_recipe = id_recipe
    ).first_or_404()

    food_recipe.id_food = request.form['id_food']
    food_recipe.id_recipe = request.form['id_recipe']

    db.session.commit()

    return 'Alimento da receita atualizado com sucesso!'


@bp_foodRecipe.route('/<int:id_food>/<int:id_recipe>/delete',
           methods=['POST'])
def delete_food_recipe(id_food, id_recipe):
    food_recipe = Food_Recipe.query.filter_by(
        id_food = id_food,
        id_recipe = id_recipe
    ).first_or_404()

    db.session.delete(food_recipe)
    db.session.commit()

    return 'Alimento removido da receita com sucesso!'