from ..extensions import db, login_manager

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime)
    id_place = db.Column(db.Integer, db.ForeignKey('place.id'))