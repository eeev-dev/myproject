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
            graduates = Graduate.query.filter_by(status='Без заявки').all()
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
                Graduate.status == 'Выбор кафедры'
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
            for graduate in Graduate.query.filter_by(supervisor=current_user.name).filter_by(status='Без заявки').all():
                graduate.status = 'Выбор кафедры'
            db.session.commit()
    else:
        flash('Установите дедлайн', 'danger')
        return render_template('graduate/topic.html', graduates=[], current_filter=filter_param)
    return render_template('graduate/topic.html', graduates=get_current_graduates(filter_param), current_filter=filter_param)


@vkr.route('/vkr/check', methods=['POST'])
def check_unique(id):
    graduate = Graduate.query.get(id)
    title = graduate.topic
    topics = Topic.query.all()
    matches = []

    for topic in topics:
        if title in topics.title:
            matches.append(topics.title)
            try:
                graduate.status = 'Подтвержден'
                graduate.message = f"Тема не прошла проверку на уникальность: {', '.join(matches)}"
                db.session.commit()
            except Exception as e:
                flash(str(e), 'danger')
                return redirect('/topics')
            flash(f'Проверка на уникальность не пройдена: {topic.title}', 'danger')
            return redirect('/topics')
        
    try:
        graduate.status = 'Проверка пройдена'
        graduate.message = ''
        db.session.commit()
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/topics')

    flash('Проверка на уникальность пройдена', 'success')
    return redirect('/topics')


@vkr.route('/vkr/add', methods=['POST'])
def add(title):
    topic = Topic(title=title)
    try:
        db.session.add(topic)
        db.session.commit()
        flash('Тема добавлена в общую таблицу', 'success')
        return redirect('/topics')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/topics')
    

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
    

@vkr.route('/vkr/<int:id>/update', methods=['POST'])
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


@vkr.route('/vkr/<int:id>/cancel', methods=['POST'])
@login_required
def down_status(id):
    graduate = Graduate.query.get_or_404(id)
    graduate.status = "Подтвержден"

    try:
        db.session.commit()
        return redirect('/vkr/topic')
    except Exception as e:
        flash(str(e), 'danger')
        print(str(e))
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
    

