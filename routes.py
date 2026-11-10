import os
from utils import app, admin_required, db, NON_VEGAN_INGREDIENTS, NON_VEGETARIAN_INGREDIENTS
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from time import sleep
import json
from fatsecret_service import obter_receitas, obter_detalhes_receitas

from models.User import User
from models.Daily_Menu import DailyMenu
from models.Nutritionist import Nutritionist
from models.Restriction import Restriction
from controllers.usuario import bp_user, bp_admin
from controllers.cardapio_diario import bp_dailyMenu
from controllers.nutricionista import bp_nutritionist, get_nutritionists
from controllers.restricao import bp_restriction

app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_admin, url_prefix='/admin')
app.register_blueprint(bp_dailyMenu, url_prefix='/dailyMenu')
app.register_blueprint(bp_nutritionist, url_prefix='/nutritionist')
app.register_blueprint(bp_restriction, url_prefix='/restriction')


@app.route('/')
def index():
    lista_colaboradores = [
        'Alba Lopes',
        'Cecília Aine',
        'Maria Luísa',
        'Thaylanne Kérrinna'
    ]
    return render_template('index.html', lista_colaboradores=lista_colaboradores)


@app.route('/paginaerro')
def paginaerro():
    return render_template('paginaerro.html')


@app.route('/homepage')
@login_required
def homepage():
    nutritionists = get_nutritionists()

    recipes = obter_receitas()

    for recipe in recipes:
        recipe['recommended'] = True
        recipe['prep_time_min'] = '0'

        r = recipe.get('recipe_id') 

        details = obter_detalhes_receitas(r)
        if not details:
            return []

        if isinstance(details, dict):
            details = [details]


        for detail in details:
            if detail.get('rating'):
                if detail.get('rating') < 4:
                    recipe['recommended'] = False
                    break

        if not recipe['recommended']:
            break

        for detail in details:
            recipe['prep_time_min'] = detail.get('preparation_time_min')
            recipe['prep_time_min'] = detail.get('preparation_time_min', '')

    return render_template('homepage.html', nutritionists=nutritionists, recipes=recipes)


@app.route('/catalogodereceitas')
@login_required
def catalogodereceitas():
    recipes = obter_receitas()

    #Recomendadas
    for recipe in recipes:
        recipe['recommended'] = True
        recipe['prep_time_min'] = '0'

        r = recipe.get('recipe_id') 

        details = obter_detalhes_receitas(r)
        if not details:
            return []

        if isinstance(details, dict):
            details = [details]

        for detail in details:
            if detail.get('rating'):
                if detail.get('rating') < 4:
                    recipe['recommended'] = False
                    break

        if not recipe['recommended']:
            break

        # Prep time
        for detail in details:
            recipe['prep_time_min'] = detail.get('preparation_time_min')
            recipe['prep_time_min'] = detail.get('preparation_time_min', '')

        # Veganas e vegetarianas
        recipe['vegan'] = True        
        recipe['vegetarian'] = True
                
        ingredients = recipe.get('recipe_ingredients', [])        
        
        if isinstance(ingredients, dict):
            ingredients = ingredients.get('ingredient', [])
        if isinstance(ingredients, dict):
            ingredients = [ingredients]

        for item in ingredients:
            ingredient_name = item.get('food_name', '') if isinstance(item, dict) else str(item)
            name_lower = ingredient_name.lower()

            if recipe['vegan']:
                for non_vegan in NON_VEGAN_INGREDIENTS:
                    if non_vegan in name_lower:
                        recipe['vegan'] = False
                        break 
            
            if recipe['vegetarian']:
                for non_vegetarian in NON_VEGETARIAN_INGREDIENTS:
                    if non_vegetarian in name_lower:
                        recipe['vegetarian'] = False
                        break

            if not recipe['vegetarian'] and not recipe['vegan']:
                break     
        

    return render_template('catalogo_de_receitas.html', recipes=recipes)


@app.route('/cardapiosemanal')
@login_required
def cardapiosemanal():
    return render_template('cardapiosemanal.html')


@app.route('/gerenciarperfil', methods=['GET', 'POST'])
@login_required
def gerenciarperfil():
    allrestrictions = Restriction.query.all()
    opcao = 'Nenhum selecionado'
    return render_template('gerenciarperfil.html', opcao=opcao, allrestrictions=allrestrictions)


@app.route('/perfilnutricionista/<int:nutritionist_crn>')
@login_required
def perfilnutricionista(nutritionist_crn):
    nutritionist = Nutritionist.query.get_or_404(nutritionist_crn)
    return render_template(
        'perfilnutricionista.html',
        nutritionist=nutritionist
    )


@app.route('/formularionutricionista')
def formulario_nutricionista():
    return render_template('formulario_nutricionista.html')