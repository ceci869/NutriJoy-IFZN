from utils import db
# from Food import Food
# from Recipe import Recipe

class FoodRecipe(db.Model):
    __tablename__ = 'FoodRecipe'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('Food.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'))

    food = db.relationship('Food', foreign_keys=food_id)
    recipe = db.relationship('Recipe', foreign_keys=recipe_id)

    def __init__(self, food_id, recipe_id):
        self.food_id = food_id
        self.recipe_id = recipe_id
    
    def __repr__(self):
        return '<Food(s) in recipe: {}>'.format(self.food_id)

