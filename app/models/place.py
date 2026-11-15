from ..extensions import db

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100))       # город, подразделение
    places = db.Column(db.Integer, nullable=False)       # свободно мест
    max_places = db.Column(db.Integer, nullable=False)   # всего мест
    requirements = db.Column(db.String(500))
    outlook = db.Column(db.String(500))
    contacts= db.Column(db.String(100))
    # Обратная связь с отзывами
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')

    @property
    def taken(self):
        return max(0, (self.max_places or 0) - (self.places or 0))
