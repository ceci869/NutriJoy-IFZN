from utils import db

class DailyMenu(db.Model):
    __tablename__ = 'DailyMenu'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    day = db.Column(db.String(7), nullable=False)
    types = db.Column(db.String(150), nullable=False)
    recipe_id = db.Column(db.String(50), nullable=False)
    recipe_name = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, day, types, recipe_id, recipe_name, user_id):
        self.user_id = user_id 
        self.day = day
        self.types = types
        self.recipe_id = recipe_id 
        self.recipe_name = recipe_name
    
    def __repr__(self):
        return '<Daily Menu: {}>'.format(self.day)