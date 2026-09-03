from utils import db

class Food(db.Model):
    __tablename__ = 'Food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    medium_price = db.Column(db.Float, nullable=False)
    season = db.Column(db.String(9), nullable=False)
    kcal = db.Column(db.Integer, nullable=False)
    total_fat = db.Column(db.Float, nullable=False)
    carbohydrate = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)

    def __init__(self, name, medium_price, season, kcal, total_fat, carbohydrate, fiber, protein):
        self.name = name
        self.medium_price = medium_price
        self.season = season
        self.kcal = kcal
        self.total_fat = total_fat
        self.carbohydrate = carbohydrate
        self.fiber = fiber
        self.protein = protein

    def __repr__(self):
        return '<Food {}>'.format(self.name)