from utils import db

class Restriction(db.Model):
    __tablename__ = 'Restriction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Restriction: {}>'.format(self.name)