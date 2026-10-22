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


def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if getattr(current_user, 'role', None) != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper