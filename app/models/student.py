from datetime import datetime
from email.policy import default

from ..extensions import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) 
    student_number = db.Column(db.String(20))
    score = db.Column(db.Numeric(8,6))
    group = db.Column(db.String(50))