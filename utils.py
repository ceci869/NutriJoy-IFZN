from flask_sqlalchemy import SQLAlchemy
from flask import Flask, abort
from flask_login import current_user, login_required
from functools import wraps

db = SQLAlchemy()
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tabelas N-N
user_restriction = db.Table(
    'UserRestriction',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('restriction_id', db.Integer, db.ForeignKey('Restriction.id'), primary_key=True)
)

# Admin
def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if getattr(current_user, 'role', None) != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper

# Lista de ingredientes não veganos
NON_VEGAN_INGREDIENTS = [
    # Meat, Poultry & Game
    'meat', 'beef', 'pork', 'chicken', 'turkey', 'duck', 'lamb', 'bacon', 
    'ham', 'sausage', 'pepperoni', 'salami', 'prosciutto', 'veal', 'mutton',

    # Seafood
    'fish', 'salmon', 'tuna', 'shrimp', 'prawns', 'crab', 'lobster', 
    'clam', 'mussel', 'oyster', 'squid', 'octopus', 'anchovy', 'anchovies', 
    'fish sauce', 'oyster sauce', 'caviar',

    # Dairy Products
    'milk', 'whole milk', 'skim milk', 'butter', 'ghee', 'cheese', 'parmesan', 
    'cheddar', 'mozzarella', 'cream', 'heavy cream', 'sour cream', 'whey', 
    'casein', 'caseinate', 'condensed milk', 'evaporated milk', 'yogurt', 'curd',
    'whey protein', 'vanilla yogurt', 'chocolate',

    # Eggs & Derivatives
    'egg', 'eggs', 'egg white', 'egg yolk', 'mayonnaise', 'albumen', 'albumin',

    # Bee Products
    'honey', 'beeswax', 'royal jelly', 'propolis',

    # Animal Fats & Gelatin
    'gelatin', 'gelatine', 'lard', 'tallow', 'suet', 'collagen', 'rennet', 

    # Hidden / Additives
    'carmine', 'cochineal', 'isinglass', 'l-cysteine', 'bone char'
]

NON_VEGETARIAN_INGREDIENTS = [
    # Meat, Poultry & Game
    'meat', 'beef', 'pork', 'chicken', 'turkey', 'duck', 'lamb', 'bacon', 
    'ham', 'sausage', 'pepperoni', 'salami', 'prosciutto', 'veal', 'mutton',
    'venison', 'bison', 'pancetta', 'chorizo', 'pastrami', 'tripe',

    # Seafood
    'fish', 'salmon', 'tuna', 'shrimp', 'prawns', 'crab', 'lobster', 
    'clam', 'mussel', 'oyster', 'squid', 'octopus', 'anchovy', 'anchovies', 
    'fish sauce', 'oyster sauce', 'caviar', 'squid ink', 'calamari', 'scallop',
    'worcestershire sauce',

    # Animal Fats & Broths
    'gelatin', 'gelatine', 'lard', 'tallow', 'suet', 'collagen', 'rennet', 
    'animal fat', 'chicken broth', 'beef broth', 'bone broth', 'chicken stock',
    'beef stock', 'pork fat', 'duck fat',

    # Hidden / Additives
    'carmine', 'cochineal', 'isinglass', 'l-cysteine', 'bone char'
]