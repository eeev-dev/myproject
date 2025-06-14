from ..extensions import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    type = db.Column(db.String(3))
    teacher = db.Column(db.String(50))
    group = db.Column(db.String(50))
    term = db.Column(db.Integer)
    day = db.Column(db.String(20))
    time = db.Column(db.String(20))
    parity = db.Column(db.String(10), default='всегда')
    is_online = db.Column(db.Integer, default=1)
    room = db.Column(db.String(20))