from flask import render_template, request, redirect, flash, url_for
from models.Food import Food
from utils import db
from flask import Blueprint

bp_food = Blueprint('food', __name__, template_folder='templates')

# =-=-=FOOD=-=-=
@bp_food.route('/add', methods=['POST', 'GET'])
def add_food():
    if request.method == 'GET':
        return render_template('alimento_add.html')

    elif request.method == 'POST':
        food = Food(
            name = request.form['name'],
            medium_price = request.form['average_value'],
            season = request.form.getlist('season'),
            kcal = request.form['kcal'],
            total_fat = request.form['fats'],
            carbohydrate = request.form['carbohydrates'],
            fiber = request.form['fibers'],
            protein = request.form['proteins']
        )

        db.session.add(food)
        db.session.commit()

        flash('Alimento adicionado com sucesso!', 'success')
        return redirect(url_for('food.get_foods'))


@bp_food.route('/get', methods=['GET'])
def get_foods():
    foods = Food.query.all()
    len_foods = len(foods)

    return render_template('alimento_get.html', foods=foods, len_foods=len_foods)


@bp_food.route('/<int:id_food>/update', methods=['POST', 'GET'])
def update_food(id_food):
    food = Food.query.get_or_404(id_food)

    if request.method == 'GET':
        return render_template('alimento_update.html', food=food)

    elif request.method == 'POST':
        name = request.form['name']
        medium_price = request.form['average_value']
        season = request.form.getlist('season')
        kcal = request.form['kcal']
        total_fat = request.form['fats']
        carbohydrate = request.form['carbohydrates']
        fiber = request.form['fibers']
        protein = request.form['proteins']

        if name:
            food.name = name
        if medium_price:
            food.medium_price = medium_price
        if season:
            food.season = ', '.join(season)
        if kcal:
            food.kcal = kcal
        if total_fat:
            food.total_fat = total_fat
        if carbohydrate:
            food.carbohydrate = carbohydrate
        if fiber:
            food.fiber = fiber
        if protein:
            food.protein = protein

        db.session.commit()

        flash('Alimento atualizado com sucesso!', 'success')
        return redirect(url_for('food.get_foods'))


@bp_food.route('/<int:id_food>/delete')
def delete_food(id_food):
    food = Food.query.get_or_404(id_food)

    db.session.delete(food)
    db.session.commit()

    flash('Alimento excluído com sucesso!', 'success')
    return redirect(url_for('food.get_foods'))