from flask import Blueprint, render_template, request, redirect, jsonify, flash, send_from_directory, current_app
from flask_login import login_required

from ..models.schedule import Schedule
from ..models.student import Student
from ..models.teacher import Teacher
from ..models.group import Group
from ..extensions import db
from flask import jsonify
import os

from datetime import datetime

schedule = Blueprint('schedule', __name__)

def extract_surname(full_name):
    return full_name.split()[0]

@schedule.route('/api/schedule', methods=['GET', 'POST'])
def get_schedule():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400
    
    student_id = data.get('student_id')

    student = Student.query.get(student_id)
    group = Group.query.filter_by(title=student.group).first()
    term = get_term(group.year)
    schedule = Schedule.query.filter_by(group=student.group).filter_by(term=term).all()

    if student and schedule:
        schedule_list = []
        for s in schedule:
            teachers = Teacher.query.all()
            link = ''
            for teacher in teachers:
                if s.teacher.replace(' ', '') == teacher.name.replace(' ', ''):
                    link = teacher.url
            schedule_list.append({
                "id": s.id,
                "title": s.title,
                "type": s.type,
                "teacher": s.teacher,
                "group": s.group,
                "term": s.term,
                "day": s.day,
                "time": s.time,
                "parity": s.parity,
                "is_online": s.is_online,
                "link": link,
                "room": s.room
            })
        return jsonify(schedule_list)
    else:
        if student == None:
            print('Студент')
        if schedule == None:
            print('Расписание')
        return '', 204
    

def get_term(year):
    month = datetime.now().month
    if month in [7, 8, 9, 10, 12]:
        return year * 2 - 1
    else:
        return year * 2
    

@schedule.route('/schedule/exam', methods=['GET', 'POST'])
def get_exams():
    data = request.get_json()
    if not data or 'student_id' not in data:
        return jsonify({"success": False, "message": "student_id отсутствует"}), 400

    student_id = data['student_id']

    try:
        student = Student.query.get(student_id)
        group = Group.query.filter_by(title=student.group).first()
        course = group.year
    except:
        return jsonify({"success": False, "message": "Нет данных для этого студента"}), 404

    # Создаём название файла на основе курса
    filename = f"Расписание{course}.docx"
    upload_path = current_app.config['UPLOAD_PATH']
    file_path = os.path.join(upload_path, filename)

    # Проверяем, существует ли файл для этого курса
    if not os.path.exists(file_path):
        return jsonify({"success": False, "message": f"Файл для курса {course} не найден"}), 404

    # Отправляем файл с нужным именем и mime-type docx
    return send_from_directory(
        directory=upload_path,
        path=filename,
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )