from flask import Blueprint, render_template, request, redirect, jsonify, flash
from flask_login import login_required

from ..models.schedule import Schedule
from ..models.student import Student
from ..models.teacher import Teacher
from ..models.group import Group
from ..extensions import db
from flask import jsonify

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