from ..extensions import db


class Intern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    place = db.Column(db.String(70))
    places = db.Column(db.Integer, default=0)
    group = db.Column(db.String(50))
    year = db.Column(db.Integer)
    head_teacher = db.Column(db.String(50))
    score = db.Column(db.Integer)
    status = db.Column(db.String(50), default='Ожидает подтверждения')