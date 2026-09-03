from utils import db
# from DailyMenu import DailyMenu
# from Recipe import Recipe

class MenuRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dailyMenu_id = db.Column(db.Integer, db.ForeignKey('DailyMenu.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'))

    dailyMenu = db.relationship('DailyMenu', foreign_keys=dailyMenu_id)
    recipe = db.relationship('Recipe', foreign_keys=recipe_id)

    def __init__(self, dailyMenu_id, recipe_id):
        self.dailyMenu_id = dailyMenu_id
        self.recipe_id = recipe_id
    
    def __repr__(self):
        return '<Recipe(s) in daily menu: {}>'.fomart(self.recipe_id)