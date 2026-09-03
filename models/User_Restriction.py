from utils import db
# from User import User
# from User_Restriction import UserRestriction

class UserRestriction(db.Model):
    __tablename__ = 'UserRestriction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    restriction_id = db.Column(db.Integer, db.ForeignKey('Restriction.id'))

    user = db.relationship('User', foreign_keys=user_id)
    restriction = db.relationship('Restriction', foreign_keys=restriction_id)

    def __init__(self, user_id, restriction_id):
        self.user_id = user_id
        self.restriction_id = restriction_id
    
    def __repr__(self):
        return '<User {} restriction(s) is {}>'.format(self.user, self.restriction_id)