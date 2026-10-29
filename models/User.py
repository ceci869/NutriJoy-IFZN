from utils import db
from flask_login import UserMixin
# from models.User_Restriction import UserRestriction
# from models.Restriction import Restriction

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='usuario')

    restrictions = db.relationship('Restriction', secondary='UserRestriction', back_populates='user')

    def __init__(self, name, email, password, cep, age):
        self.name = name
        self.email = email
        self.password = password
        self.cep = cep
        self.age = age

    def __repr__(self):
        return '<Usuário {}>'.format(self.name)