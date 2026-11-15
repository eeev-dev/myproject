from app import create_app, db
from app.models import student, group, place, review, deadline  # noqa: F401

app = create_app()

with app.app_context():
    db.create_all()
    print("Все таблицы созданы!")
