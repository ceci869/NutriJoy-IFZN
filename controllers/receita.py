# from flask import render_template, request, redirect, flash, url_for
# from models.Recipe import Recipe
# from models.Food import Food
# from models.Restriction import Restriction
# from utils import db
# from flask import Blueprint

# bp_recipe = Blueprint('recipe', __name__, template_folder='templates')

# # =-=-=RECIPE=-=-=
# @bp_recipe.route('/add', methods=['POST', 'GET'])
# def add_recipe():
#     allfoods = Food.query.all()
#     allrestrictions = Restriction.query.all()
#     if request.method == 'GET':
#         return render_template('receitas_add.html', allfoods=allfoods, allrestrictions=allrestrictions)
    
#     elif request.method == 'POST':

#         name = request.form['name'],
#         medium_price = request.form['average_value']
#         foods_ids = request.form.getlist('foods')
#         restrictions_ids = request.form.getlist('restrictions')

#         recipe = Recipe(name=name, medium_price=medium_price)
#         selected_foods = Food.query.filter(Food.id.in_(foods_ids)).all()
#         selected_restrictions = Restriction.query.filter(Restriction.id.in_(restrictions_ids)).all()

#         recipe.food.extend(selected_foods)
#         recipe.restrictions.extend(selected_restrictions)

#         db.session.add(recipe)
#         db.session.commit()

#         flash('Receita adicionada com sucesso!', 'success')
#         return redirect(url_for('recipe.get_recipes'))


# @bp_recipe.route('/get')
# def get_recipes():
#     recipes = Recipe.query.all()
#     len_recipes = len(recipes)

#     return render_template('receitas_get.html', recipes=recipes, len_recipes=len_recipes)


# @bp_recipe.route('/<int:id_recipe>/update', methods=['POST'])
# def update_recipe(id_recipe):
#     recipe = Recipe.query.get_or_404(id_recipe)

#     recipe.id_nutritionist = request.form['id_nutritionist']
#     recipe.name = request.form['name']
#     recipe.average_value = request.form['average_value']
#     recipe.kcal = request.form['kcal']
#     recipe.fats = request.form['fats']
#     recipe.carbohydrates = request.form['carbohydrates']
#     recipe.fibers = request.form['fibers']
#     recipe.proteins = request.form['proteins']

#     db.session.commit()

#     return 'Receita atualizada com sucesso!'


# @bp_recipe.route('/<int:id_recipe>/delete', methods=['POST'])
# def delete_recipe(id_recipe):
#     recipe = Recipe.query.get_or_404(id_recipe)

#     db.session.delete(recipe)
#     db.session.commit()

#     return 'Receita excluída com sucesso!'