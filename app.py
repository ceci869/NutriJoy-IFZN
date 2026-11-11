import json
from utils import db, app
import os
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, current_user
from flask_login import login_user, login_required, logout_user, current_user

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_mydb = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

lm = LoginManager(app)
lm.login_view = 'user.verificalogin'

conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}:{db_port}/{db_mydb}"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

import routes
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
    
if __name__ == "__main__":
    app.start(debug=True)