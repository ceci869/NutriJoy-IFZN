from utils import db

class Restriction(db.Model):
    __tablename__ = 'Restriction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

    user = db.relationship('User', secondary='UserRestriction', back_populates='restrictions')
    recipes = db.relationship('Recipe', secondary='RecipeRestriction', back_populates='restrictions')

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Restriction: {}>'.format(self.name)