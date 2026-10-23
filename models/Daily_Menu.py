from utils import db

class DailyMenu(db.Model):
    __tablename__ = 'DailyMenu'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    day = db.Column(db.String(7), nullable=False)

    user = db.relationship('User', back_populates='daily_menu')
    recipes = db.relationship('Recipe', secondary='MenuRecipe', back_populates='daily_menu')

    def __init__(self, day, user_id):
        self.user_id = user_id 
        self.day = day
    
    def __repr__(self):
        return '<Daily Menu: {}>'.fomart(self.day)