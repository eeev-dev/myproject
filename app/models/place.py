from email.policy import default

from ..extensions import db

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100))
    places = db.Column(db.Integer, nullable=False)
    max_places = db.Column(db.Integer, nullable=False)
    requirements = db.Column(db.String(500))
    outlook = db.Column(db.String(500))
    contacts= db.Column(db.String(100))
    # Обратная связь с отзывами
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')