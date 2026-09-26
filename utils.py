from flask_sqlalchemy import SQLAlchemy
from flask import Flask
db = SQLAlchemy()
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER