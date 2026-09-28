from utils import db
from flask_login import UserMixin
from models.User_Restriction import UserRestriction
from models.Restriction import Restriction

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    restricoes = db.relationship(
        'Restriction',
        secondary=UserRestriction,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Usuário {}>'.format(self.name)