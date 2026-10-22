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