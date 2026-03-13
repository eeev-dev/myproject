from flask_login import login_user, logout_user, current_user, login_required
from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
from ..functions import calculate_term, find_teacher_and_subject, extract_subject, extract_teacher
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
from ..models.intern import Intern
from ..models.graduate import Graduate
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
            flash(f'Ошибка при обновлении группы: {str(e)}', 'danger')
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
        flash(f'Запись не была удалена: {str(e)}', 'danger')
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

        try:
            # Чтение CSV с удалением BOM
            file.stream.seek(0)  # вернуться в начало файла
            stream = io.StringIO(file.stream.read().decode("utf-8-sig"), newline=None)
            reader = csv.reader(stream)

            unique_groups = {}  # словарь: {title: year}

            for i, row in enumerate(reader, start=1):
                try:
                    # Проверка на пустую или короткую строку
                    if not row or len(row) < 2:
                        flash(f"Строка {i} пропущена: недостаточно столбцов", "warning")
                        continue

                    title = row[1].strip()
                    year_str = row[0].strip()
                    if not year_str:
                        flash(f"Строка {i} пропущена: пустой год", "warning")
                        continue

                    year = year_str[0]  # берем только первый символ года

                    # Добавляем только уникальные title
                    if title not in unique_groups:
                        unique_groups[title] = year

                except Exception as e:
                    flash(f"Ошибка в строке {i}: {e}", "danger")

            # Вставка уникальных групп в базу
            for title, year in unique_groups.items():
                try:
                    group = Group(title=title, year=year)
                    db.session.add(group)
                except Exception as e:
                    flash(f"Ошибка при добавлении группы '{title}': {e}", "danger")

            try:
                db.session.commit()
                flash(f"Импортировано {len(unique_groups)} уникальных групп", "success")
                return redirect('/admin/groups')
            except Exception as e:
                db.session.rollback()
                flash(f"Ошибка при сохранении в базе данных: {e}", "danger")

        except Exception as e:
            flash(f"Ошибка при чтении CSV: {e}", "danger")
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
            flash(f'Ошибка при обновлении преподавателя: {str(e)}', 'danger')
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
        flash(f'Запись не была удалена: {str(e)}', 'danger')
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
        file.stream.seek(0)
        content = file.stream.read().decode("utf-8-sig")
        reader = csv.reader(content.splitlines())

        try:
            for row in reader:
                teacher = Teacher(
                    name=row[0],
                    url=row[1]
                )
                db.session.add(teacher)

            try:
                db.session.commit()
                flash("Данные успешно загружены", 'success')
                return redirect('/admin/teachers')
            except Exception as e:
                flash(f'Ошибка при добавлении: {str(e)}', 'danger')
            
        except Exception as e:
            flash(f"Ошибка при обработке CSV: {e}", "danger")

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
            flash(f'Ошибка при обновлении студента: {str(e)}', 'danger')
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
        flash(f'Ошибка при удалении студента: {str(e)}', 'danger')
        return redirect('/admin/students')


@admin.route('/load/students', methods=['GET', 'POST'])
@login_required
def upload_students():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or not file.filename.endswith('.csv'):
            flash('Загрузите корректный CSV-файл', 'danger')
            return redirect(request.url)

        try:
            # Очистка таблицы Student и сброс последовательности
            db.session.query(Student).delete()
            db.session.execute(text("ALTER SEQUENCE student_id_seq RESTART WITH 1"))

            # Опционально: очистка других связанных таблиц
            db.session.query(Intern).delete()
            db.session.query(Graduate).delete()
            db.session.commit()

            # Чтение CSV с удалением BOM
            file.stream.seek(0)
            content = file.stream.read().decode("utf-8-sig")
            reader = csv.reader(content.splitlines())

            for i, row in enumerate(reader, start=1):
                try:
                    # Проверка на пустую или некорректную строку
                    if not row or len(row) < 4:
                        flash(f"Строка {i} пропущена: недостаточно столбцов", "warning")
                        continue

                    # Сохраняем данные студента
                    name = row[2].strip()
                    group = row[1].strip()
                    student_number = row[3].strip()

                    if not name or not group or not student_number:
                        flash(f"Строка {i} пропущена: пустые поля", "warning")
                        continue

                    # Создаем Student
                    student = Student(
                        name=name,
                        group=group,
                        student_number=student_number
                    )
                    db.session.add(student)
                    db.session.flush()  # чтобы получить student.id до commit

                    # Создаем Intern
                    try:
                        year = int(row[0].strip()[0])
                    except Exception:
                        flash(f"Строка {i}: неверный формат года '{row[0]}'", "warning")
                        year = None

                    intern = Intern(
                        student_id=student.id,
                        name=name,
                        group=group,
                        year=year
                    )
                    db.session.add(intern)

                    # Создаем Graduate
                    graduate = Graduate(
                        student_id=student.id,
                        name=name,
                        group=group,
                    )
                    db.session.add(graduate)

                except Exception as e:
                    flash(f"Ошибка в строке {i}: {e}", "danger")

            # Сохраняем все записи
            try:
                db.session.commit()
                flash("Данные успешно загружены", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Ошибка при сохранении в базе данных: {e}", "danger")

        except Exception as e:
            flash(f"Ошибка при обработке CSV: {e}", "danger")

        return redirect('/admin/students')

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
            flash(f'Ошибка при обновлении расписания: {str(e)}', 'danger')
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
        flash(f'Запись не была удалена: {str(e)}', 'danger')
        return redirect('/admin/schedule')


@admin.route('/load/schedule', methods=['GET', 'POST'])
@login_required
def upload_schedule():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or not file.filename.endswith('.csv'):
            flash('Загрузите корректный CSV-файл', 'danger')

        # Очистка таблицы
        db.session.query(Schedule).delete()
        db.session.execute(text("ALTER SEQUENCE schedule_id_seq RESTART WITH 1"))

        # Чтение CSV-файла без сохранения
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        reader = csv.reader(stream)

        try:
            # Чтение CSV с удалением BOM
            file.stream.seek(0)  # вернуться в начало файла
            stream = io.StringIO(file.stream.read().decode("utf-8-sig"), newline=None)
            reader = csv.reader(stream)

            for row in reader:
                if len(row) < 4:
                    continue

                time = row[0].strip()
                group = re.search(r'группа:\s*([^,]+)', row[1])
                day = row[2].strip()
                lesson_text = row[3].strip()

                if not lesson_text:
                    continue

                group_csv = group.group(1) if group else ""

                group_bd = Group.query.filter_by(title=group_csv).first()

                if not group_bd:
                    flash(f"Группа '{group}' не найдена. Загрузите ее в разделе 'Группы'", "warning")
                    continue

                term = calculate_term(csv_term_is_autumn=("Осен" in row[1]), year=int(group_bd.year))

                # тип занятия
                type_match = re.search(r'\[(.*?)\]', lesson_text)
                lesson_type = type_match.group(1) if type_match else ""

                # аудитория
                if re.search(r'\bonline\b', lesson_text, re.IGNORECASE):
                    room = ""
                else:
                    room_match = re.search(r'ауд\.\s*([^\s]+)', lesson_text)
                    room = room_match.group(1) if room_match else ""

                # преподаватель (Фамилия И.О.)
                teacher_match = re.search(r'([А-ЯЁ][а-яё]+\s+[А-Я]\.[А-Я]\.)', lesson_text)
                teacher = teacher_match.group(1) if teacher_match else ""

                # название предмета
                title = lesson_text
                title = re.sub(r'\[.*?\]', '', title)        # убрать [Лк], [нед...]
                title = re.sub(r'[А-ЯЁ][а-яё]+\s+[А-Я]\.[А-Я]\.', '', title)  # убрать преподавателя
                title = re.sub(r'\s*ауд\..*$', '', title)    # убрать аудиторию
                title = re.sub(r'\bonline\b', '', title, flags=re.IGNORECASE)
                title = re.sub(r'\s+', ' ', title).strip()

                schedule = Schedule(
                    title=title,
                    type=lesson_type,
                    teacher=teacher,
                    group=group_bd.title,
                    term=term,
                    day=day,
                    time=time,
                    parity="всегда",
                    is_online=1 if "nline" in row[3] else 0,
                    room=room
                )

                db.session.add(schedule)

            try:
                db.session.commit()
                flash("Данные успешно загружены", 'success')
                return redirect('/admin/schedule')
            except Exception as e:
                db.session.rollback()
                flash(f"Ошибка при сохранении в базе данных: {e}", "danger")

        except Exception as e:
            flash(f"Ошибка при чтении CSV: {e}", "danger")
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
            flash(str(e), 'danger')
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
        flash(f'Запись не была удалена: {str(e)}', 'danger')
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