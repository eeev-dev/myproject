from flask_login import login_user, logout_user, current_user, login_required
from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
import csv
import io
from flask import Blueprint, render_template, redirect, flash, url_for, request
from sqlalchemy import text

from ..models.user import User
from ..models.group import Group
from ..models.teacher import Teacher
from ..models.student import Student

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
