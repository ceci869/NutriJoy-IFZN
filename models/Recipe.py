from utils import db

class Recipe(db.Model):
    __tablename__ = 'Recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    medium_price = db.Column(db.Float, nullable=False)

    restrictions = db.relationship('Restriction', secondary='RecipeRestriction', back_populates='recipes')
    food = db.relationship('Food', secondary='FoodRecipe', back_populates='recipes')
    daily_menu = db.relationship('DailyMenu', secondary='MenuRecipe', back_populates='recipes')

    def __init__(self, name, medium_price, kcal, total_fat, fiber, protein):
        self.name = name
        self.medium_price = medium_price
        self.kcal = kcal
        self.total_fat = total_fat
        self.fiber = fiber
        self.protein = protein
    
    def __repr__(self):
        return '<Recipe: {}>'.format(self.name)