from flask import Blueprint, render_template, request, redirect, jsonify, flash
from flask_login import login_required, current_user
from flask_wtf import file
from sqlalchemy import text
from sqlalchemy import desc, or_

from ..models.student import Student
from ..models.group import Group
from ..extensions import db

student = Blueprint('student', __name__)


@student.route('/ping', methods=['GET', 'POST'])
def ping():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400

    student_id = data.get('student_id')
    student = Student.query.get(int(student_id))
    if student:
        return jsonify({
            "success": True,
            "message": "Сервер запущен"
        }), 200
    else:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401
    

@student.route('/student/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400

    student_number = data.get('student_number')
    student = Student.query.filter_by(student_number=student_number).first()
    if student:
        return jsonify({
            "success": True,
            "id": student.id,
            "message": "Авторизация успешна"
        }), 200
    else:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401