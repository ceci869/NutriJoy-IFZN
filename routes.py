from utils import app
from flask import render_template, url_for, redirect, request
from flask_login import login_required
import json

from models.User import User
from models.Daily_Menu import DailyMenu
from models.Recipe import Recipe
from models.Food import Food
from models.Nutritionist import Nutritionist
from models.Restriction import Restriction
from models.User_Restriction import UserRestriction
from models.Menu_Recipe import MenuRecipe
from models.Food_Recipe import FoodRecipe
from controllers.usuario import bp_user
from controllers.alimento import bp_food
from controllers.cardapio_diario import bp_dailyMenu
from controllers.nutricionista import bp_nutritionist, get_nutritionists
from controllers.receita import bp_recipe
from controllers.restricao import bp_restriction
from controllers.usuario_restricao import bp_userRestriction
from controllers.comida_receita import bp_foodRecipe
from controllers.receita_cardapio import bp_menuRecipe

app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_food, url_prefix='/food')
app.register_blueprint(bp_dailyMenu, url_prefix='/dailyMenu')
app.register_blueprint(bp_nutritionist, url_prefix='/nutritionist')
app.register_blueprint(bp_recipe, url_prefix='/recipe')
app.register_blueprint(bp_restriction, url_prefix='/restriction')
app.register_blueprint(bp_userRestriction, url_prefix='/user_restriction')
app.register_blueprint(bp_menuRecipe, url_prefix='/menu_recipe')
app.register_blueprint(bp_foodRecipe, url_prefix='/food_recipe')


@app.route('/')
def index():
    lista_colaboradores = ['Alba Lopes', 'Cecília Aine', 'Maria Luísa', 'Thaylanne Kérrinna']
    return render_template('index.html', lista_colaboradores=lista_colaboradores)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/paginaerro')
def paginaerro():
    return render_template('paginaerro.html')

@app.route('/homepage')
@login_required
def homepage():
    nutritionists = get_nutritionists()
    return render_template('homepage.html', nutritionists=nutritionists)

@app.route('/catalogodereceitas')
@login_required
def catalogodereceitas():
    lista_receitas = [
        {'nome':'Sanduíches kawaii',
         'foto':url_for('static', filename='img/receita1.jpg')         
        },
        {
         'nome':'Pizza kawaii',
         'foto':url_for('static', filename='img/receita2.jpg')
        },
        {
         'nome':'Curry kawaii',
         'foto':url_for('static', filename='img/receita3.jpg')
        },
        {
         'nome':'Sushi kawaii',
         'foto':url_for('static', filename='img/receita4.jpg')
        },
        {
         'nome':'Pudim kawaii',
         'foto':url_for('static', filename='img/receita5.jpg')
        }
    ]

    return render_template('catalogo_de_receitas.html', lista_receitas=lista_receitas)

@app.route('/cardapiosemanal')
@login_required
def cardapiosemanal():
    return render_template('cardapiosemanal.html')

@app.route('/gerenciarperfil', methods=['GET', 'POST'])
@login_required
def gerenciarperfil():
    opcao = 'Nenhum selecionado'
    return render_template('gerenciarperfil.html', opcao=opcao)

@app.route('/perfilnutricionista')
@login_required
def perfilnutricionista():
    return render_template('perfilnutricionista.html')

@app.route('/formularionutricionista')
def formulario_nutricionista():
    return render_template('formulario_nutricionista.html')