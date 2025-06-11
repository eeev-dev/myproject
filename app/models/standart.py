from ..extensions import db

class Standart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    taken = db.Column(db.Integer, default=0)