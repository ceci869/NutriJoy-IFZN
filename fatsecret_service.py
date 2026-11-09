import os
import requests

CLIENT_ID = os.environ.get('FATSECRET_CLIENT_ID')
CLIENT_SECRET = os.environ.get('FATSECRET_CLIENT_SECRET')

TOKEN_URL = 'https://oauth.fatsecret.com/connect/token'
API_BASE_URL = 'https://platform.fatsecret.com/rest/server.api'

def obter_access_token():
    payload = {
        'grant_type': 'client_credentials'
    }

    try:
        response = requests.post(
            TOKEN_URL,
            data=payload,
            auth=(CLIENT_ID, CLIENT_SECRET),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )

        if response.status_code != 200:
            print(f'Erro OAuth ({response.status_code}): {response.text}')

        response.raise_for_status()
        return response.json().get('access_token')

    except requests.exceptions.RequestException as e:
        print(f'Não foi possível realizar a autenticação FatSecret: {e}')
        return None


# Get de Receitas (Catálogo)

def obter_receitas(number=40, standard_term=''):
    token = obter_access_token()

    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'method': 'recipes.search.v3',
        'search_expression': standard_term,
        'max_results': number,
        'format': 'json',
        'region': 'BR',
        'language': 'pt'
    }

    try:
        response = requests.get(API_BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        print('Resposta FatSecret', data)

        recipes = data.get('recipes', {})
        if not recipes or 'recipe' not in recipes:
            return []

        recipes_in_recipes = recipes['recipe']

        if isinstance(recipes_in_recipes, dict):
            recipes_in_recipes = [recipes_in_recipes]

        return recipes_in_recipes

    except requests.exceptions.RequestException as e:
        print(f'Não foi possível realizar a autenticação FatSecret: {e}')
        return None     

def obter_todas_receitas(page_number, standard_term=''):
    token = obter_access_token()

    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'method': 'recipes.search.v3',
        'search_expression': standard_term,
        'page_number': page_number,
        'format': 'json',
        'region': 'BR',
        'language': 'pt'
    }

    try:
        response = requests.get(API_BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        print('Resposta FatSecret', data)

        recipes = data.get('recipes', {})
        if not recipes or 'recipe' not in recipes:
            return []

        recipes_in_recipes = recipes['recipe']

        if isinstance(recipes_in_recipes, dict):
            recipes_in_recipes = [recipes_in_recipes]

        return recipes_in_recipes

    except requests.exceptions.RequestException as e:
        print(f'Não foi possível realizar a autenticação FatSecret: {e}')
        return None

# Detalhes de uma receita
def obter_detalhes_receitas(recipe_id):

    token = obter_access_token()

    if not token:
        print('Não foi possível obter o token da FatSecret.')
        return None

    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'method': 'recipe.get.v2',
        'recipe_id': recipe_id,
        'format': 'json',
        'region': 'BR',
        'language': 'pt'
    }

    try:
        response = requests.get(
            API_BASE_URL,
            headers=headers,
            params=params
        )

        response.raise_for_status()
        data = response.json()

        print('\n========== RESPOSTA DA FATSECRET ==========')
        print(data)
        print('============================================\n')

        recipe = data.get('recipe')

        if not recipe:
            print('A API não retornou os dados da receita.')
            return None

        if isinstance(recipe, list):
            recipe = recipe[0] if recipe else None

        if not isinstance(recipe, dict):
            print('Formato inesperado dos dados da receita.')
            return None

        print('INGREDIENTES:', recipe.get('recipe_ingredients'))
        print('MODO DE PREPARO:', recipe.get('recipe_directions'))

        return recipe

    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar detalhes da receita: {e}')
        return None