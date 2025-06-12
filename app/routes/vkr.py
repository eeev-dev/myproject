from flask import Blueprint, render_template, request, redirect, jsonify, flash
from ..extensions import db
from sqlalchemy import or_
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import text

from ..models.graduate import Graduate
from ..models.topic import Topic
from ..models.standart import Standart
from ..models.student import Student
from ..models.group import Group
from ..models.user import User
from ..models.teacher import Teacher

vkr = Blueprint('vkr', __name__)

#Сайт

#Научный руководитель

def get_graduates(filter_param):
    graduates = Graduate.query
    if filter_param == 'none':
        return graduates.filter(
            or_(
                Graduate.status == 'Без заявки',
                Graduate.status == 'Выбор кафедры'
            )
        ).all()
    elif filter_param == 'pending':
        return graduates.filter_by(status='Ожидает подтверждения').all()
    elif filter_param == 'confirmed':
        return graduates.filter_by(status='Подтвержден').all()


@vkr.route('/vkr/supervisor', methods=['GET'])
def supervisor():
    filter_param = request.args.get('filter', 'pending')
    if current_user.supervisor_deadline is not None:
        if datetime.utcnow() < current_user.supervisor_deadline:
            return render_template('graduate/supervisor.html', graduates=get_graduates(filter_param), current_filter=filter_param)
        else:
            graduates = Graduate.query.filter(or_(Graduate.status == 'Без заявки', Graduate.status == 'Ожидает подтверждения')).all()
            for graduate in graduates:
                graduate.status = 'Выбор кафедры'
            try:
                db.session.commit()
                return render_template('graduate/supervisor.html', get_graduates(filter_param), current_filter=filter_param)
            except Exception as e:
                flash(str(e), 'danger')
                return render_template('graduate/supervisor.html', graduates=[], current_filter=filter_param)
    else:
        flash('Установите дедлайн', 'danger')
        return render_template('graduate/supervisor.html', graduates=[], current_filter=filter_param)


@vkr.route('/vkr/<int:id>/update', methods=['POST'])
@login_required
def upgrade_status(id):
    graduate = Graduate.query.get_or_404(id)
    graduate.status = "Подтвержден"

    try:
        db.session.commit()
        return redirect('/vkr/supervisor')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/vkr/supervisor')


@vkr.route('/vkr/<int:id>/cancel', methods=['POST'])
@login_required
def downgrade_status(id):
    graduate = Graduate.query.get_or_404(id)
    graduate.status = "Без заявки"

    try:
        db.session.commit()
        return redirect('/vkr/supervisor')
    except Exception as e:
        flash(str(e), 'danger')
        print(str(e))
        return redirect('/vkr/supervisor')


@vkr.route('/vkr/<int:id>/force-supervisor', methods=['POST'])
def force_supervisor(id):
    graduate = Graduate.query.get_or_404(id)
    graduate.supervisor = current_user.name
    graduate.status = "Подтвержден"
    try:
        db.session.commit()
        flash(f'Научный руководитель студента {graduate.name}: {graduate.supervisor}', 'success')
        return render_template('graduate/supervisor.html', current_filter='none')
    except Exception as e:
        flash(str(e), 'danger')
        return render_template('graduate/supervisor.html', current_filter='none')
    

# Тема

def get_current_graduates(filter_param):
    graduates = Graduate.query.filter_by(supervisor=current_user.name)
    if filter_param == 'none':
        return graduates.filter(
            or_(
                Graduate.status == 'Подтвержден',
                Graduate.status == 'Выбор темы'
            )
        ).all()
    elif filter_param == 'pending':
        return graduates.filter_by(status='Ожидает проверки').all()
    elif filter_param == 'confirmed':
        return graduates.filter_by(status='Проверка пройдена').all()


@vkr.route('/vkr/topic', methods=['GET'])
def topic():
    filter_param = request.args.get('filter', 'pending')
    if current_user.vkr_deadline is not None:
        if datetime.utcnow() > current_user.vkr_deadline:
            for graduate in Graduate.query.filter_by(supervisor=current_user.name).filter(or_(Graduate.status == 'Без заявки', Graduate.status == 'Ожидает подтверждения')).all():
                graduate.status = 'Выбор темы'
                graduate.message = 'Свяжитесь по поводу темы с научным руководителем'
            db.session.commit()
    else:
        flash('Установите дедлайн', 'danger')
        return render_template('graduate/topic.html', graduates=[], current_filter=filter_param)
    return render_template('graduate/topic.html', graduates=get_current_graduates(filter_param), current_filter=filter_param)


@vkr.route('/vkr/<int:id>/check', methods=['POST'])
def check_unique(id):
    graduate = Graduate.query.get(id)
    title = graduate.topic
    topics = Topic.query.all()
    matches = []

    for topic in topics:
        if title in topic.title:
            matches.append(topics.title)
            try:
                graduate.status = 'Подтвержден'
                graduate.message = f"Тема не прошла проверку на уникальность: {', '.join(matches)}"
                db.session.commit()
            except Exception as e:
                flash(str(e), 'danger')
                return redirect('/vkr/topic')
            flash(f'Проверка на уникальность не пройдена: {topic.title}', 'danger')
            return redirect('/vkr/topic')
        
    try:
        graduate.status = 'Проверка пройдена'
        graduate.message = ''
        db.session.commit()
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/vkr/topic')

    flash('Проверка на уникальность пройдена', 'success')
    return redirect('/vkr/topic')


@vkr.route('/vkr/<title>/add', methods=['POST'])
def add(title):
    topic = Topic(title=title)
    try:
        db.session.add(topic)
        db.session.commit()
        flash('Тема добавлена в общую таблицу', 'success')
        return redirect('/vkr/topic')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/vkr/topic')
    

@vkr.route('/vkr/<int:id>/force', methods=['GET', 'POST'])
def force(id):
    graduate = Graduate.query.get_or_404(id)
    standarts = Standart.query.filter_by(taken=0).all()
    if request.method == 'POST':
        if request.form.get('name') != graduate.group:
            graduate.group = request.form.get('group')
        if request.form.get('group') != graduate.group:
            graduate.group = request.form.get('group')

        graduate.topic = request.form['topic']
        topic = Standart.query.filter_by(title=graduate.topic).first()
        topic.taken = 1
        graduate.status = 'Проверка пройдена'
        try:
            db.session.commit()
        except Exception as e:
            flash(str(e), 'danger')
            return redirect('/vkr/topic')

        return redirect('/vkr/topic')
    else:
        return render_template('graduate/force_topic.html', graduate=graduate, topics=[s.title for s in standarts])
    

@vkr.route('/vkr/<int:id>/update-topic', methods=['POST'])
@login_required
def up_status(id):
    graduate = Graduate.query.get_or_404(id)
    graduate.status = "Проверка пройдена"

    try:
        db.session.commit()
        return redirect('/vkr/topic')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/vkr/topic')


@vkr.route('/vkr/<int:id>/cancel-topic', methods=['POST'])
@login_required
def down_status(id):
    graduate = Graduate.query.get_or_404(id)
    graduate.status = "Подтвержден"
    graduate.topic = None

    try:
        db.session.commit()
        return redirect('/vkr/topic')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/vkr/topic')


@vkr.route('/vkr/upload', methods=['GET'])
def upload_graduates():
    groups = Group.query.filter_by(year=4).all()
    students = []
    for group in groups:
        group_students = Student.query.filter_by(group=group.title).all()
        students.extend(group_students)

    # Очистка таблицы
    db.session.query(Graduate).delete()
    db.session.execute(text("ALTER SEQUENCE graduate_id_seq RESTART WITH 1"))

    for student in students:
        graduate = Graduate(
            student_id=student.id,
            name = student.name,
            group = student.group,
            status = 'Без заявки'
        )
        db.session.add(graduate)

    try:
        db.session.commit()
        flash('Данные успешно загружены', 'success')
        return redirect('/vkr/supervisor')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/vkr/supervisor')


# API

@vkr.route('/vkr/get', methods=['GET', 'POST'])
def get_graduate():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400
    student_id = data.get('student_id')
    graduate = Graduate.query.filter_by(student_id=student_id).first()
    user = User.query.get(1)
    if graduate and user:
        return jsonify({
            "supervisor_deadline": user.supervisor_deadline,
            "topic_deadline": user.vkr_deadline,
            "supervisor": graduate.supervisor,
            "topic": graduate.topic,
            "status": graduate.status,
            "message": graduate.message,
            "success": True
        }), 200
    else:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401


@vkr.route('/vkr/post-supervisor', methods=['GET', 'POST'])
def post_supervisor():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400
    student_id = data.get('student_id')
    supervisor = data.get('supervisor_name')

    graduate = Graduate.query.filter_by(student_id=student_id).first()

    if graduate:
        try:
            graduate.supervisor = supervisor
            graduate.status = 'Ожидает подтверждения'
            db.session.commit()
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 401
        
        return jsonify({
            "success": True,
            "message": "Ок"
        }), 200
    else:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401
    

@vkr.route('/vkr/post-topic', methods=['GET', 'POST'])
def post_topic():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400
    
    student_id = data.get('student_id')
    topic = data.get('topic')

    graduate = Graduate.query.filter_by(student_id=student_id).first()

    if graduate:
        try:
            graduate.topic = topic
            graduate.status = 'Ожидает проверки'
            db.session.commit()
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 401

        return jsonify({
            "success": True,
            "message": "Ок"
        }), 200
    else:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401
    

@vkr.route('/api/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    teachers_list = [teacher.name for teacher in teachers]
    return jsonify(teachers_list)
