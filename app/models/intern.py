from datetime import datetime
from email.policy import default

from ..extensions import db


class Intern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(20))
    name = db.Column(db.String(50))
    place = db.Column(db.String(70))
    group = db.Column(db.String(50))
    year = db.Column(db.Integer)
    head_teacher = db.Column(db.String(50))
    score = db.Column(db.Numeric(8,6))
    letter = db.Column(db.String(200))
    status = db.Column(db.String(50), default='Без заявки')
    message = db.Column(db.String(200))