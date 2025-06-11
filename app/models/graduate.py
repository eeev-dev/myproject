from ..extensions import db

class Graduate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) 
    group = db.Column(db.String(50))
    topic = db.Column(db.String(200))
    supervisor = db.Column(db.String(50))
    status = db.Column(db.String(50))
    message = db.Column(db.String(200))