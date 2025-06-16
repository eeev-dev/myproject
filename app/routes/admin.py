from flask_login import login_user, logout_user, current_user, login_required
from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
from ..functions import find_teacher_and_subject, extract_subject, extract_teacher
import csv
import io
from flask import Blueprint, render_template, redirect, flash, url_for, request, current_app
import os
import re
from sqlalchemy import text

from ..models.user import User
from ..models.group import Group
from ..models.teacher import Teacher
from ..models.student import Student
from ..models.schedule import Schedule
from ..models.topic import Topic

admin = Blueprint('admin', __name__)


@admin.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user.role == None or user.role == 'user':
            user.role = 'user'
            db.session.commit()
            flash('Войдите как преподаватель', 'danger')
            return render_template('user/login.html', form=form)
        else:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('admin.panel'))
            else:
                flash(str(form.errors), "danger")
    return render_template('admin/login.html', form=form)


@admin.route('/admin/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/user/login')


# Группы

@admin.route('/admin/groups', methods=['GET', 'POST'])
@login_required
def panel():
    groups = Group.query.all()
    return render_template('admin/group/table.html', groups=groups)


@admin.route('/groups/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    group = Group.query.get(id)
    if request.method == 'POST':
        group.id = request.form['id']  # Обязательное
        group.title = request.form['title']  # Обязательное
        group.year = request.form['year']  # Обязательное
        group.head_teacher = request.form['head_teacher']  # Обязательное

        try:
            db.session.commit()
            return redirect('/admin/groups')
        except Exception as e:
            print(str(e))
    else:
        return render_template('admin/group/edit.html', group=group)


@admin.route('/groups/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    group = Group.query.get(id)
    try:
        db.session.delete(group)
        db.session.commit()
        flash('Успех', 'success')
        return redirect('/admin/groups')
    except Exception as e:
        print(str(e))
        flash('Запись не была удалена', 'danger')
        return redirect('/admin/groups')


@admin.route('/load/groups', methods=['GET', 'POST'])
@login_required
def upload_groups():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or not file.filename.endswith('.csv'):
            flash('Загрузите корректный CSV-файл', 'danger')

        # Очистка таблицы
        db.session.query(Group).delete()
        db.session.execute(text("ALTER SEQUENCE group_id_seq RESTART WITH 1"))

        # Чтение CSV-файла без сохранения
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        reader = csv.reader(stream)

        for row in reader:
            group = Group(
                title=row[0],
                year=row[1]
            )
            db.session.add(group)

        db.session.commit()
        flash("Данные успешно загружены", 'success')
        return redirect('/admin/groups')
    else:
        return render_template('admin/group/load.html')

#Преподаватели
 
@admin.route('/admin/teachers', methods=['GET', 'POST'])
@login_required
def teachers():
    teachers = Teacher.query.all()
    return render_template('admin/teacher/table.html', teachers=teachers)


@admin.route('/teachers/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_teacher(id):
    teacher = Teacher.query.get(id)
    if request.method == 'POST':
        teacher.id = request.form['id']  # Обязательное
        teacher.name = request.form['name']  # Обязательное
        teacher.url = request.form['url']  # Обязательное

        try:
            db.session.commit()
            return redirect('/admin/teachers')
        except Exception as e:
            print(str(e))
    else:
        return render_template('admin/teacher/edit.html', teacher=teacher)


@admin.route('/groups/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_teacher(id):
    group = Group.query.get(id)
    try:
        db.session.delete(group)
        db.session.commit()
        flash('Успех', 'success')
        return redirect('/admin/teachers')
    except Exception as e:
        print(str(e))
        flash('Запись не была удалена', 'danger')
        return redirect('/admin/teachers')


@admin.route('/load/teachers', methods=['GET', 'POST'])
@login_required
def upload_teachers():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or not file.filename.endswith('.csv'):
            flash('Загрузите корректный CSV-файл', 'danger')

        # Очистка таблицы
        db.session.query(Teacher).delete()
        db.session.execute(text("ALTER SEQUENCE teacher_id_seq RESTART WITH 1"))

        # Чтение CSV-файла без сохранения
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        reader = csv.reader(stream)

        for row in reader:
            teacher = Teacher(
                name=row[0],
                url=row[1]
            )
            db.session.add(teacher)

        db.session.commit()
        flash("Данные успешно загружены", 'success')
        return redirect('/admin/teachers')
    else:
        return render_template('admin/teacher/load.html')
    
#Студенты
 
@admin.route('/admin/students', methods=['GET', 'POST'])
@login_required
def students():
    students = Student.query.all()
    return render_template('admin/student/table.html', students=students)


@admin.route('/students/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_student(id):
    student = Student.query.get(id)
    if request.method == 'POST':
        student.id = request.form['id']
        student.name = request.form['name']
        student.student_number = request.form['student_number']
        student.score = request.form['score']
        student.group = request.form['group']

        try:
            db.session.commit()
            return redirect('/admin/students')
        except Exception as e:
            print(str(e))
    else:
        return render_template('admin/student/edit.html', student=student)


@admin.route('/students/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    student = Student.query.get(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Успех', 'success')
        return redirect('/admin/students')
    except Exception as e:
        print(str(e))
        flash('Запись не была удалена', 'danger')
        return redirect('/admin/students')


@admin.route('/load/students', methods=['GET', 'POST'])
@login_required
def upload_students():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or not file.filename.endswith('.csv'):
            flash('Загрузите корректный CSV-файл', 'danger')

        # Очистка таблицы
        db.session.query(Teacher).delete()
        db.session.execute(text("ALTER SEQUENCE student_id_seq RESTART WITH 1"))

        # Чтение CSV-файла без сохранения
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        reader = csv.reader(stream)

        for row in reader:
            student = Student(
                name=row[0],
                group=row[1],
                student_number=row[2],
                score=row[3]
            )
            db.session.add(student)

        db.session.commit()
        flash("Данные успешно загружены", 'success')
        return redirect('/admin/students')
    else:
        return render_template('admin/student/load.html')
    
# Расписание

@admin.route('/admin/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    schedule = Schedule.query.all()
    return render_template('admin/schedule/table.html', schedule=schedule)


@admin.route('/schedule/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_schedule(id):
    schedule_item = Schedule.query.get(id)
    if request.method == 'POST':
        schedule_item.id = request.form['id']
        schedule_item.title = request.form['title']
        schedule_item.type = request.form['type']
        schedule_item.teacher = request.form['teacher']
        schedule_item.group = request.form['group']
        schedule_item.term = request.form['term']
        schedule_item.day = request.form['day']
        schedule_item.time = request.form['time']
        schedule_item.parity = request.form['parity']
        schedule_item.is_online = request.form['is_online']
        schedule_item.room = request.form['room']

        try:
            db.session.commit()
            return redirect('/admin/schedule')
        except Exception as e:
            print(str(e))
    else:
        return render_template('admin/schedule/edit.html', schedule_item=schedule_item)


@admin.route('/schedule/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_schedule_item(id):
    schedule_item = Schedule.query.get(id)
    try:
        db.session.delete(schedule_item)
        db.session.commit()
        flash('Успех', 'success')
        return redirect('/admin/schedule')
    except Exception as e:
        print(str(e))
        flash('Запись не была удалена', 'danger')
        return redirect('/admin/schedule')


@admin.route('/load/schedule', methods=['GET', 'POST'])
@login_required
def upload_schedule():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or not file.filename.endswith('.csv'):
            flash('Загрузите корректный CSV-файл', 'danger')

        # Чтение CSV-файла без сохранения
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        reader = csv.reader(stream)

        next(reader)

        for row in reader:
            if len(row) > 3 and row[3].strip():
                year = 4
                column1 = row[0].strip()
                column2 = row[1].strip()
                column3 = row[2].strip()
                column4 = row[3].strip()
                str = find_teacher_and_subject(column4)
                schedule = Schedule(
                    title=extract_subject(str).strip(),
                    type=column4[1:3],
                    teacher=extract_teacher(str),
                    group=column2[-11:],
                    term=year * 2 if 'Вес' in column2 else year * 2 - 1,
                    day=column3,
                    time=column1,
                    parity='всегда',
                    is_online=0 if column4[-1:].isdigit() else 1,
                    room=column4[-5:] if column4[-1:].isdigit() else None
                )
                db.session.add(schedule)

        db.session.commit()
        flash("Данные успешно загружены", 'success')
        return redirect('/admin/schedule')

    else:
        return render_template('admin/schedule/load.html')
    
#Расписание экзаменов

@admin.route('/admin/exam', methods=['GET', 'POST'])
def save_schedule():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Файл не найден в запросе", 'danger')
            return redirect('/admin/exam')

        file = request.files['file']

        # Проверка расширения .docx
        if not file.filename.endswith('.docx'):
            flash('Допустим только .docx файл', 'danger')
            return redirect('/admin/exam')

        # Проверка названия: Расписание1.docx ... Расписание4.docx
        filename = file.filename
        if not re.fullmatch(r"Расписание[1-4]\.docx", filename):
            flash("Название файла должно быть 'Расписание' + цифра от 1 до 4", 'danger')
            return redirect('/admin/exam')

        upload_path = current_app.config['UPLOAD_PATH']
        os.makedirs(upload_path, exist_ok=True)

        save_path = os.path.join(upload_path, filename)
        file.save(save_path)

        flash("Файл успешно сохранён", 'success')
        return redirect('/admin/exam')

    # Если GET — возвращаем HTML-шаблон
    return render_template('admin/exam/exam.html')


@admin.route('/admin/clear-exams', methods=['POST'])
def clear_schedules():
    upload_path = current_app.config['UPLOAD_PATH']

    if not os.path.exists(upload_path):
        flash('Папка загрузки не найдена', 'danger')
        return redirect('/admin/exam')

    deleted_files = []
    for filename in os.listdir(upload_path):
        if "Расписание" in filename:
            file_path = os.path.join(upload_path, filename)
            try:
                os.remove(file_path)
                deleted_files.append(filename)
            except Exception as e:
                flash(f"Ошибка при удалении {filename}: {str(e)}", 'danger')
                return redirect('/admin/exam')

    if deleted_files:
        flash(f"Удалены файлы: {', '.join(deleted_files)}", 'success')
        return redirect('/admin/exam')
    else:
        flash("Нет файлов для удаления", 'danger')
        return redirect('/admin/exam')
    
# Темы ВКР

@admin.route('/admin/topics', methods=['GET', 'POST'])
@login_required
def topics():
    topics = Topic.query.all()
    return render_template('admin/topic/table.html', topics=topics)


@admin.route('/topic/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_topics(id):
    topic = Topic.query.get(id)
    if request.method == 'POST':
        topic.id = request.form['id']
        topic.title = request.form['title']

        try:
            db.session.commit()
            return redirect('/admin/topics')
        except Exception as e:
            print(str(e))
    else:
        return render_template('admin/topic/edit.html', topic=topic)


@admin.route('/topic/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_topic(id):
    topic = Topic.query.get(id)
    try:
        db.session.delete(topic)
        db.session.commit()
        flash('Успех', 'success')
        return redirect('/admin/topics')
    except Exception as e:
        print(str(e))
        flash('Запись не была удалена', 'danger')
        return redirect('/admin/topics')


@admin.route('/load/topics', methods=['GET', 'POST'])
@login_required
def upload_topics():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or not file.filename.endswith('.csv'):
            flash('Загрузите корректный CSV-файл', 'danger')

        # Очистка таблицы
        db.session.query(Topic).delete()
        db.session.execute(text("ALTER SEQUENCE topic_id_seq RESTART WITH 1"))

        # Чтение CSV-файла без сохранения
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        reader = csv.reader(stream)

        for row in reader:
            topic = Topic(
                title=row[0]
            )
            db.session.add(topic)

        db.session.commit()
        flash("Данные успешно загружены", 'success')
        return redirect('/admin/topics')
    else:
        return render_template('admin/topic/load.html')