from flask_sqlalchemy import SQLAlchemy
from flask import Flask
db = SQLAlchemy()
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tabelas N-N

user_restriction = db.Table('UserRestriction',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('restriction_id', db.Integer, db.ForeignKey('Restriction.id'), primary_key=True)
)

recipe_restriction = db.Table('RecipeRestriction',
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipe.id'), primary_key = True),
    db.Column('restriction_id', db.Integer, db.ForeignKey('Restriction.id'), primary_key=True)
)

menu_recipe = db.Table('MenuRecipe',
    db.Column('menu_id', db.Integer, db.ForeignKey('DailyMenu.id'), primary_key = True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipe.id'), primary_key = True)
)

food_recipe = db.Table('FoodRecipe',
    db.Column('food_id', db.Integer, db.ForeignKey('Food.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipe.id', primary_key=True))
)