from ..extensions import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    student_number = db.Column(db.String(20))
    group = db.Column(db.String(50))

    # Поля, перенесённые из интерна
    place = db.Column(db.String(70))          # выбранное место практики или 'Свое место практики'
    title = db.Column(db.String(70))          # название своего места практики
