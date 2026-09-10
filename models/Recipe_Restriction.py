from utils import db

class RecipeRestriction(db.Model):
    __tablename__ = 'Recipe_Restriction'
    id = db.Column(db.Integer, primary_key=True)
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    restriction_id = db.Column(db.Integer, db.ForeignKey('Restriction.id'))

    recipe = db.relationship('Recipe', foreign_keys=recipe_id)
    restriction = db.relationship('Restriction', foreign_keys=restriction_id)

    def __init__(self, recipe_id, restriction_id):
        self.recipe_id = recipe_id
        self.restriction_id = restriction_id
    
    def __repr__(self):
        return '<Restriction(s) in recipe: {}>'.fomart(self.recipe_id) 