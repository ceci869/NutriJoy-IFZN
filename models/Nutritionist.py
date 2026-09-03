from utils import db
from flask_login import UserMixin
# from User import User

class Nutritionist(UserMixin, db.Model):
    __tablename__ = 'Nutritionist'
    crn = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    specialization = db.Column(db.String(60), nullable=False)
    contributions = db.Column(db.Integer, nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, user_id, name, email, password, specialization, contributions, experience_years):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.specialization = specialization
        self.contributions = contributions
        self.experience_years = experience_years

    def __repr__(self):
        return '<Nutritionist {}>'.format(self.name)