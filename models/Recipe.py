from utils import db

class Recipe(db.Model):
    __tablename__ = 'Recipe'
    id = db.Column(db.Integer, primary_key=True)
    nutritionist_id = db.Column(db.Integer, db.ForeignKey('Nutritionist.crn'))
    name = db.Column(db.String(50), nullable=False)
    medium_price = db.Column(db.Float, nullable=False)
    kcal = db.Column(db.Integer, nullable=False)
    total_fat = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)

    nutritionist = db.relationship('Nutritionist', foreign_keys=nutritionist_id)

    def __init__(self, nutritionist_id, name, medium_price, kcal, total_fat, fiber, protein):
        self.nutritionist_id = nutritionist_id
        self.name = name
        self.medium_price = medium_price
        self.kcal = kcal
        self.total_fat = total_fat
        self.fiber = fiber
        self.protein = protein
    
    def __repr__(self):
        return '<Recipe: {}>'.format(self.name)