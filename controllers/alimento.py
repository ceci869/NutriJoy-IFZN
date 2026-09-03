from flask import render_template, request, redirect
from models.Food import Food
from utils import db
from flask import Blueprint

bp_food = Blueprint('food', __name__, template_folder='templates')

# =-=-=FOOD=-=-=
@bp_food.route('/fadd', methods=['POST'])
def add_food():
    food = Food(
        name = request.form['name'],
        average_value = request.form['average_value'],
        portion = request.form['portion'],
        kcal = request.form['kcal'],
        fats = request.form['fats'],
        carbohydrates = request.form['carbohydrates'],
        fibers = request.form['fibers'],
        proteins = request.form['proteins']
    )

    db.session.add(food)
    db.session.commit()

    return 'Alimento adicionado com sucesso!'


@bp_food.route('/foods')
def get_foods():
    foods = Food.query.all()

    return str(foods)


@bp_food.route('/<int:id_food>/update', methods=['POST'])
def update_food(id_food):
    food = Food.query.get_or_404(id_food)

    food.name = request.form['name']
    food.average_value = request.form['average_value']
    food.portion = request.form['portion']
    food.kcal = request.form['kcal']
    food.fats = request.form['fats']
    food.carbohydrates = request.form['carbohydrates']
    food.fibers = request.form['fibers']
    food.proteins = request.form['proteins']

    db.session.commit()

    return 'Alimento atualizado com sucesso!'


@bp_food.route('/<int:id_food>/delete', methods=['POST'])
def delete_food(id_food):
    food = Food.query.get_or_404(id_food)

    db.session.delete(food)
    db.session.commit()

    return 'Alimento excluído com sucesso!'