import os
import requests
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from threading import Lock
from time import monotonic

CLIENT_ID = os.environ.get('FATSECRET_CLIENT_ID')
CLIENT_SECRET = os.environ.get('FATSECRET_CLIENT_SECRET')

TOKEN_URL = 'https://oauth.fatsecret.com/connect/token'
API_BASE_URL = 'https://platform.fatsecret.com/rest/server.api'

_token_lock = Lock()
_access_token = None
_access_token_expires_at = 0

_recipe_details_lock = Lock()
_recipe_details_cache = {}
_RECIPE_DETAILS_CACHE_TTL = 3600
_RECIPE_DETAILS_CACHE_MAX_SIZE = 256


def obter_access_token():
    global _access_token, _access_token_expires_at

    with _token_lock:
        if _access_token and monotonic() < _access_token_expires_at:
            return _access_token

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
            token_data = response.json()
            token = token_data.get('access_token')
            expires_in = token_data.get('expires_in', 0)

            if token and isinstance(expires_in, (int, float)):
                _access_token = token
                _access_token_expires_at = monotonic() + max(0, expires_in - 60)

            return token

        except requests.exceptions.RequestException as e:
            print(f'Não foi possível realizar a autenticação FatSecret: {e}')
            return None


def _buscar_detalhes_receitas(recipe_id):
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
        response = requests.get(API_BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        recipe = data.get('recipe')

        if not recipe:
            print('A API não retornou os dados da receita.')
            return None

        if isinstance(recipe, list):
            recipe = recipe[0] if recipe else None

        if not isinstance(recipe, dict):
            print('Formato inesperado dos dados da receita.')
            return None

        return recipe

    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar detalhes da receita: {e}')
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
    cache_key = str(recipe_id)
    now = monotonic()

    with _recipe_details_lock:
        cached = _recipe_details_cache.get(cache_key)
        if cached and now < cached[0]:
            return deepcopy(cached[1])
        _recipe_details_cache.pop(cache_key, None)

    recipe = _buscar_detalhes_receitas(cache_key)
    if recipe is None:
        return None

    with _recipe_details_lock:
        if len(_recipe_details_cache) >= _RECIPE_DETAILS_CACHE_MAX_SIZE:
            _recipe_details_cache.pop(next(iter(_recipe_details_cache)))
        _recipe_details_cache[cache_key] = (
            monotonic() + _RECIPE_DETAILS_CACHE_TTL,
            deepcopy(recipe)
        )

    return recipe


def obter_detalhes_receitas_em_lote(recipe_ids):
    cache_keys = list(dict.fromkeys(
        str(recipe_id) for recipe_id in recipe_ids if recipe_id is not None
    ))
    if not cache_keys:
        return {}

    with ThreadPoolExecutor(max_workers=min(5, len(cache_keys))) as executor:
        details = executor.map(obter_detalhes_receitas, cache_keys)
        return dict(zip(cache_keys, details))
