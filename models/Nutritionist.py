from utils import db
from flask_login import UserMixin

class Nutritionist(UserMixin, db.Model):
    __tablename__ = 'Nutritionist'
    crn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(60))
    experience_years = db.Column(db.Integer, nullable=False)
    foto_perfil = db.Column(db.String(100), nullable=False)

    def __init__(self, crn, name, email, specialization, experience_years, foto_perfil):
        self.crn = crn
        self.name = name
        self.email = email
        self.specialization = specialization
        self.experience_years = experience_years
        self.foto_perfil = foto_perfil

    def __repr__(self):
        return '<Nutritionist {}>'.format(self.name)