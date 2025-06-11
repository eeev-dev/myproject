from ..extensions import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    head_teacher = db.Column(db.String(50))