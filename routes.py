import os
from dotenv import load_dotenv
from utils import app, admin_required, db, NON_VEGAN_INGREDIENTS, NON_VEGETARIAN_INGREDIENTS
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from time import sleep
import json
from fatsecret_service import (
    obter_receitas,
    obter_todas_receitas,
    obter_detalhes_receitas,
    obter_detalhes_receitas_em_lote,
)
from flask import render_template, url_for, redirect, request, flash, jsonify
from groq import Groq

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

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

ai_content = 'You are a helpful chatbot that only speaks in Portuguese (Brazil). Only answer questions related to: nutrition, nutrition in childhood and nutrition in adolescence. If you are asked about other things answer "Desculpe, mas não forneço esse tipo de informação". Be objective in your answers.'
client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def index():
    lista_colaboradores = [
        'Alba Lopes',
        'Cecília Aine',
        'Maria Luísa',
        'Thaylanne Kérrinna'
    ]
    nutritionists = get_nutritionists()
    return render_template(
        'index.html',
        lista_colaboradores=lista_colaboradores,
        nutritionists=nutritionists
    )


@app.route('/paginaerro')
def paginaerro():
    return render_template('paginaerro.html')


@app.route('/homepage')
@login_required
def homepage():
    nutritionists = get_nutritionists()
    recipes = obter_receitas()
    details_by_recipe_id = obter_detalhes_receitas_em_lote(
        recipe.get('recipe_id') for recipe in recipes
    )

    for recipe in recipes:
        recipe['recommended'] = True
        recipe['prep_time_min'] = ''

        recipe_id = recipe.get('recipe_id')
        details = details_by_recipe_id.get(str(recipe_id))

        if isinstance(details, list):
            details = details[0] if details else {}

        if isinstance(details, dict) and 'recipe' in details:
            details = details['recipe']

        if not isinstance(details, dict):
            details = {}

        rating = details.get('rating')

        if rating:
            try:
                if float(rating) < 4:
                    recipe['recommended'] = False
            except (ValueError, TypeError):
                pass

        recipe['prep_time_min'] = details.get(
            'preparation_time_min', ''
        )

    # Buscar receitas salvas no cardápio semanal
    saved_recipes = DailyMenu.query.filter_by(
        user_id=current_user.id
    ).all()
    menu_details_by_recipe_id = obter_detalhes_receitas_em_lote(
        item.recipe_id for item in saved_recipes
    )

    menu_dict = {}
    imagens_cache = {}

    for item in saved_recipes:
        if item.day not in menu_dict:
            menu_dict[item.day] = {}

        if item.types not in menu_dict[item.day]:
            menu_dict[item.day][item.types] = []

        # Buscar imagem da receita
        if item.recipe_id not in imagens_cache:
            details = menu_details_by_recipe_id.get(str(item.recipe_id))

            if isinstance(details, list):
                details = details[0] if details else {}

            if isinstance(details, dict) and 'recipe' in details:
                details = details['recipe']

            if not isinstance(details, dict):
                details = {}

            imagens_cache[item.recipe_id] = extrair_imagem_receita(details)

        item.recipe_image = imagens_cache[item.recipe_id]

        menu_dict[item.day][item.types].append(item)

    return render_template(
        'homepage.html',
        nutritionists=nutritionists,
        recipes=recipes,
        menu_dict=menu_dict
    )

@app.route('/catalogodereceitas')
@login_required
def catalogodereceitas():
    recipes = obter_receitas()
    details_by_recipe_id = obter_detalhes_receitas_em_lote(
        recipe.get('recipe_id') for recipe in recipes
    )

    for recipe in recipes:
        recipe['recommended'] = True
        recipe['prep_time_min'] = ''

        recipe_id = recipe.get('recipe_id')

        details = details_by_recipe_id.get(str(recipe_id))

        if isinstance(details, list):
            details = details[0] if details else {}

        if isinstance(details, dict) and 'recipe' in details:
            details = details['recipe']

        if not isinstance(details, dict):
            details = {}

        # Avaliação
        rating = details.get('rating') or recipe.get('rating')

        if rating:
            try:
                if float(rating) < 4:
                    recipe['recommended'] = False
            except (ValueError, TypeError):
                pass

        # Tempo de preparo
        recipe['prep_time_min'] = (
            details.get('preparation_time_min')
            or recipe.get('preparation_time_min')
            or details.get('cooking_time_min')
            or recipe.get('cooking_time_min')
            or ''
        )

        # Veganas e vegetarianas
        recipe['vegan'] = True
        recipe['vegetarian'] = True

        ingredients = details.get('ingredients', recipe.get('recipe_ingredients', []))

        if isinstance(ingredients, dict):
            ingredients = ingredients.get('ingredient', [])

        if isinstance(ingredients, dict):
            ingredients = [ingredients]

        for item in ingredients:
            ingredient_name = item.get('food_name', '') if isinstance(item, dict) else str(item)
            name_lower = ingredient_name.lower()

            if any(non_vegan in name_lower for non_vegan in NON_VEGAN_INGREDIENTS):
                recipe['vegan'] = False

            if any(non_vegetarian in name_lower for non_vegetarian in NON_VEGETARIAN_INGREDIENTS):
                recipe['vegetarian'] = False

    return render_template('catalogo_de_receitas.html', recipes=recipes)


@app.route('/cardapiosemanal')
@login_required
def cardapiosemanal():
    user_id = current_user.id
    saved_recipes = DailyMenu.query.filter_by(user_id=user_id).all()

    menu_dict = {}
    for item in saved_recipes:
        if item.day not in menu_dict:
            menu_dict[item.day] = {}
        if item.types not in menu_dict[item.day]:
            menu_dict[item.day][item.types] = []

        menu_dict[item.day][item.types].append(item)

    return render_template('cardapiosemanal.html', menu_dict=menu_dict, saved_recipes=saved_recipes)

# Chatbot da página do cardápio semanl
@app.route('/chatbot_nutrijoy', methods=['POST'])
def chatbot_nutrijoy():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'Mensagem vazia'}), 400

    try:
        stream = client.chat.completions.create(
                model='openai/gpt-oss-120b', 
                messages=[
                    {'role': 'system', 'content': ai_content},
                    {'role': 'user', 'content': user_input}
                ],
                temperature=0.5,
                max_completion_tokens=2048,
                stream=False
        )

        chatbot_reply = stream.choices[0].message.content
        return jsonify({'reply': chatbot_reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500   

def extrair_imagem_receita(recipe):
    images = recipe.get('recipe_image') or recipe.get('recipe_images')

    if isinstance(images, dict):
        images = (
            images.get('recipe_image')
            or images.get('image_url')
            or images.get('url')
        )

    if isinstance(images, list):
        images = images[0] if images else None

    if isinstance(images, dict):
        images = images.get('image_url') or images.get('url')

    return images if isinstance(images, str) else None
    


@app.route('/escolhareceitas')
@login_required
def escolhareceitas():
    day = request.args.get('day')
    meal_type = request.args.get('meal_type')

    page_number = int(request.args.get('page', 0))
    termo = request.args.get('busca', '')

    recipes = obter_todas_receitas(page_number, termo) or []
    details_by_recipe_id = obter_detalhes_receitas_em_lote(
        recipe.get('recipe_id') for recipe in recipes
    )

    # Ingredientes que indicam presença de lactose
    ingredientes_com_lactose = [
        'milk', 'leite', 'cheese', 'queijo',
        'butter', 'manteiga', 'cream', 'creme de leite',
        'yogurt', 'iogurte', 'whey', 'soro de leite',
        'casein', 'caseína', 'lactose',
        'milk powder', 'leite em pó',
        'condensed milk', 'leite condensado',
        'evaporated milk', 'buttermilk',
        'nata', 'requeijão'
    ]

    # Leites vegetais que não devem ser classificados como lactose
    leites_vegetais = [
        'leite de coco',
        'leite de soja',
        'leite de amêndoas',
        'leite de aveia',
        'leite de arroz',
        'leite vegetal',
        'coconut milk',
        'soy milk',
        'almond milk',
        'oat milk',
        'rice milk'
    ]

    for recipe in recipes:

        # Imagem da receita
        recipe['recipe_image'] = extrair_imagem_receita(recipe)

        # Tempo de preparo
        recipe['prep_time_min'] = (
            recipe.get('preparation_time_min')
            or recipe.get('cooking_time_min')
            or ''
        )

        try:
            # Busca os detalhes da receita
            recipe_id = recipe.get('recipe_id')
            details = details_by_recipe_id.get(str(recipe_id))

            if isinstance(details, list):
                details = details[0] if details else {}

            if isinstance(details, dict) and 'recipe' in details:
                details = details['recipe']

            if not isinstance(details, dict):
                details = {}

            # Completa imagem e tempo com os detalhes
            if not recipe['recipe_image']:
                recipe['recipe_image'] = extrair_imagem_receita(details)

            if not recipe['prep_time_min']:
                recipe['prep_time_min'] = (
                    details.get('preparation_time_min')
                    or details.get('cooking_time_min')
                    or ''
                )

            # Obtém os ingredientes
            ingredientes = (
                details.get('recipe_ingredients')
                or details.get('ingredients')
                or recipe.get('recipe_ingredients')
                or recipe.get('ingredients')
                or []
            )

            if isinstance(ingredientes, dict):
                ingredientes = ingredientes.get('ingredient', [ingredientes])

            if isinstance(ingredientes, dict):
                ingredientes = [ingredientes]

            nomes_ingredientes = []

            for ingrediente in ingredientes:
                if isinstance(ingrediente, dict):
                    nome = (
                        ingrediente.get('food_name')
                        or ingrediente.get('ingredient_description')
                        or ingrediente.get('name')
                        or ingrediente.get('description')
                        or ''
                    )
                else:
                    nome = str(ingrediente)

                if nome:
                    nomes_ingredientes.append(nome.lower())

            # Só classifica quando existem ingredientes disponíveis
            ingredientes_disponiveis = len(nomes_ingredientes) > 0

            # Verifica se é vegetariana
            possui_carne = any(
                item.lower() in nome
                for nome in nomes_ingredientes
                for item in NON_VEGETARIAN_INGREDIENTS
            )

            recipe['vegetarian'] = (
                ingredientes_disponiveis and not possui_carne
            )

            # Verifica se é vegana
            possui_ingrediente_nao_vegano = any(
                item.lower() in nome
                for nome in nomes_ingredientes
                for item in NON_VEGAN_INGREDIENTS
            )

            recipe['vegan'] = (
                ingredientes_disponiveis
                and not possui_ingrediente_nao_vegano
                and recipe['vegetarian']
            )

            # Verifica se é sem lactose
            possui_lactose = False

            for nome in nomes_ingredientes:

                # Ignora leites de origem vegetal
                if any(leite in nome for leite in leites_vegetais):
                    continue

                if any(
                    ingrediente in nome
                    for ingrediente in ingredientes_com_lactose
                ):
                    possui_lactose = True
                    break

            recipe['lactose_free'] = (
                ingredientes_disponiveis and not possui_lactose
            )

        except Exception as e:
            print(f"Erro ao buscar detalhes da receita: {e}")

            recipe['vegetarian'] = False
            recipe['vegan'] = False
            recipe['lactose_free'] = False

    return render_template(
        'escolha_receitas.html',
        recipes=recipes,
        current_page=page_number,
        termo_busca=termo,
        day=day,
        meal_type=meal_type
    )


@app.route('/salvarreceitacardapio', methods=['POST'])
@login_required
def salvar_receita_cardapio():
    user_id = current_user.id
    day = request.form.get('day')
    meal_type = request.form.get('meal_type')

    recipe_ids = request.form.getlist('recipe_id')
    recipe_names = request.form.getlist('recipe_name')

    if not recipe_ids:
        flash('Selecione pelo menos uma receita.', 'warning')
        return redirect(url_for('cardapiosemanal'))

    try:
        for recipe_id, recipe_name in zip(recipe_ids, recipe_names):
            new_item = DailyMenu(
                day=day,
                types=meal_type,
                user_id=user_id,
                recipe_id=recipe_id,
                recipe_name=recipe_name
            )

            db.session.add(new_item)

        db.session.commit()
        flash('Receitas adicionadas ao cardápio!', 'success')

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar receitas: {e}")
        flash('Não foi possível adicionar as receitas.', 'error')

    return redirect(url_for('cardapiosemanal'))

@app.route('/removerreceita/<int:item_id>', methods=['POST'])
@login_required
def remover_do_cardapio(item_id):
    dailymenu_recipe = DailyMenu.query.get_or_404(item_id)

    db.session.delete(dailymenu_recipe)
    db.session.commit()

    flash('Receita removida', 'success')
    return redirect(url_for('cardapiosemanal'))

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


@app.route('/perfilnutricionista/publico/<int:nutritionist_crn>')
def perfilnutricionista_publico(nutritionist_crn):
    nutritionist = Nutritionist.query.get_or_404(nutritionist_crn)
    return render_template(
        'perfilnutricionista_publico.html',
        nutritionist=nutritionist
    )


@app.route('/formularionutricionista')
def formulario_nutricionista():
    return render_template('formulario_nutricionista.html')


@app.route('/receita/<int:recipe_id>')
@login_required
def detalhes_receita(recipe_id):
    recipe = obter_detalhes_receitas(recipe_id)

    if not recipe:
        return redirect(url_for('catalogodereceitas'))

    # Caso a resposta ainda esteja dentro da chave recipe
    if 'recipe' in recipe:
        recipe = recipe['recipe']

    # Imagem
    images = recipe.get('recipe_images', {})
    if isinstance(images, dict):
        images = images.get('recipe_image', [])

    if isinstance(images, str):
        images = [images]

    recipe_image = images[0] if images else None

    # Ingredientes
    ingredients = recipe.get('ingredients', {})

    if isinstance(ingredients, dict):
        ingredients = ingredients.get('ingredient', [])

    if isinstance(ingredients, dict):
        ingredients = [ingredients]

    # Modo de preparo
    directions = recipe.get('directions', {})

    if isinstance(directions, dict):
        directions = directions.get('direction', [])

    if isinstance(directions, dict):
        directions = [directions]

    return render_template(
        'detalhes_receita.html',
        recipe=recipe,
        recipe_image=recipe_image,
        ingredients=ingredients,
        directions=directions
    )

@app.route('/receita/<int:recipe_id>/detalhes-json')
@login_required
def detalhes_receita_json(recipe_id):
    details = obter_detalhes_receitas(recipe_id)

    if not details:
        return jsonify({'erro': 'Não foi possível carregar os detalhes da receita.'}), 404

    if isinstance(details, list):
        details = details[0] if details else {}

    if isinstance(details, dict) and 'recipe' in details:
        details = details['recipe']

    if not isinstance(details, dict):
        return jsonify({'erro': 'Formato de receita inválido.'}), 404

    ingredients = details.get('ingredients', {})

    if isinstance(ingredients, dict):
        ingredients = ingredients.get('ingredient', [])

    if isinstance(ingredients, dict):
        ingredients = [ingredients]

    directions = details.get('directions', {})

    if isinstance(directions, dict):
        directions = directions.get('direction', [])

    if isinstance(directions, dict):
        directions = [directions]

    nutrition = details.get('nutrition', {})

    if not isinstance(nutrition, dict):
        nutrition = {}

    return jsonify({
        'recipe_id': details.get('recipe_id'),
        'recipe_name': details.get('recipe_name', ''),
        'recipe_description': details.get('recipe_description', ''),
        'recipe_image': extrair_imagem_receita(details),
        'preparation_time_min': details.get('preparation_time_min', ''),
        'cooking_time_min': details.get('cooking_time_min', ''),
        'servings': details.get('number_of_servings') or details.get('servings', ''),
        'nutrition': {
            'calories': nutrition.get('calories', ''),
            'carbohydrate': nutrition.get('carbohydrate', ''),
            'protein': nutrition.get('protein', ''),
            'fat': nutrition.get('fat', ''),
            'fiber': nutrition.get('fiber', ''),
            'sugar': nutrition.get('sugar', '')
        },
        'ingredients': [
            {
                'name': item.get('food_name', ''),
                'quantity': item.get('measurement_description', ''),
                'units': item.get('number_of_units', '')
            }
            for item in ingredients
            if isinstance(item, dict)
        ],
        'directions': [
            {
                'number': item.get('direction_number', ''),
                'description': item.get('direction_description', '')
            }
            for item in directions
            if isinstance(item, dict)
        ]
    })