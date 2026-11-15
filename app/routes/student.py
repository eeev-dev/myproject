from flask import Blueprint, jsonify

from ..api_errors import ApiError, payload
from ..models.student import Student

student = Blueprint('student', __name__)


@student.route('/ping', methods=['GET', 'POST'])
def ping():
    data = payload()
    try:
        student_id = int(data.get('student_id'))
    except (TypeError, ValueError):
        raise ApiError("Не указан или некорректен student_id", 400)

    if not Student.query.get(student_id):
        raise ApiError("Студент не найден. Войдите заново", 401)
    return jsonify({"success": True, "message": "Сервер запущен"}), 200


@student.route('/student/login', methods=['GET', 'POST'])
def login():
    data = payload()

    student_number = str(data.get('student_number') or '').strip()
    if not student_number:
        raise ApiError("Введите номер студенческого билета", 400)

    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        raise ApiError("Студент с таким номером не найден", 401)

    return jsonify({
        "success": True,
        "id": student.id,
        "name": student.name,
        "message": "Авторизация успешна"
    }), 200
