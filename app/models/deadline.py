from ..extensions import db


class Deadline(db.Model):
    """Сроки практики. Используется одна (последняя) запись."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))              # название практики
    apply_start = db.Column(db.Date)               # начало набора
    apply_end = db.Column(db.Date)                 # конец набора
    practice_start = db.Column(db.Date)            # начало прохождения
    practice_end = db.Column(db.Date)              # конец прохождения

    @staticmethod
    def current():
        return Deadline.query.order_by(Deadline.id.desc()).first()

    @property
    def apply_set(self):
        return bool(self.apply_start and self.apply_end)

    @property
    def practice_set(self):
        return bool(self.practice_start and self.practice_end)
