"""Пошаговая настройка практики (шаги 1–6)."""
import csv
import os
from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, url_for, request, current_app, send_from_directory, abort
from flask_login import login_required
from sqlalchemy import text, func
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models.student import Student
from ..models.group import Group
from ..models.place import Place
from ..models.deadline import Deadline
from .. import state
from .admin import fill_place, delete_place_record

steps = Blueprint('steps', __name__, url_prefix='/admin/steps')

INSTRUCTION_EXTENSIONS = {'.pdf', '.doc', '.docx', '.png', '.jpg', '.jpeg', '.xlsx', '.xls', '.txt'}


@steps.before_request
@login_required
def _require_login():
    pass


def _safe_name(filename):
    """secure_filename выбрасывает кириллицу — оставляем буквы любых алфавитов."""
    name = os.path.basename(filename or '').strip().replace('/', '_').replace('\\', '_')
    if name in ('', '.', '..') or name.startswith('.'):
        return secure_filename(filename or '') or None
    return name


@steps.route('/')
def index():
    for s in state.steps_state():
        if s['state'] != 'done':
            return redirect(url_for(f'steps.step{s["n"]}'))
    return redirect(url_for('steps.step1'))


# ---------- Шаг 1. Загрузка студентов (логика загрузки файла прежняя) ----------

def _reset_sequence(name):
    if db.engine.dialect.name == 'postgresql':
        db.session.execute(text(f"ALTER SEQUENCE {name}_id_seq RESTART WITH 1"))


@steps.route('/1', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or not file.filename.endswith('.csv'):
            flash('Загрузите корректный CSV-файл', 'danger')
            return redirect(request.url)

        try:
            # Очистка таблицы Student и сброс последовательности
            db.session.query(Student).delete()
            _reset_sequence('student')
            db.session.commit()

            # Чтение CSV с удалением BOM
            file.stream.seek(0)
            content = file.stream.read().decode("utf-8-sig")
            reader = csv.reader(content.splitlines())

            group_years = {}
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

                    student = Student(
                        name=name,
                        group=group,
                        student_number=student_number,
                    )
                    db.session.add(student)
                    db.session.flush()

                    year_str = row[0].strip()
                    if group not in group_years:
                        group_years[group] = int(year_str[0]) if year_str[:1].isdigit() else None

                except Exception as e:
                    flash(f"Ошибка в строке {i}: {e}", "danger")

            # Группы, которых ещё нет, создаются автоматически
            existing = {g.title for g in Group.query.all()}
            for title, year in group_years.items():
                if title not in existing:
                    db.session.add(Group(title=title, year=year))

            # Все места снова свободны
            for p in Place.query.all():
                p.places = p.max_places

            try:
                db.session.commit()
                flash("Данные успешно загружены", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Ошибка при сохранении в базе данных: {e}", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при обработке CSV: {e}", "danger")

        return redirect(url_for('steps.step1'))

    total = Student.query.count()
    groups = []
    for (title, count) in (db.session.query(Student.group, func.count(Student.id))
                           .group_by(Student.group).order_by(Student.group).all()):
        names = [s.name for s in Student.query.filter_by(group=title).order_by(Student.name).limit(3)]
        groups.append({'title': title, 'count': count, 'names': names, 'more': max(0, count - len(names))})
    return render_template('admin/steps/step1.html', current=1, total=total, groups=groups,
                           replace=request.args.get('replace'))


# ---------- Шаг 2. Руководители групп ----------

@steps.route('/2', methods=['GET', 'POST'])
def step2():
    groups = Group.query.order_by(Group.title).all()
    if request.method == 'POST':
        for g in groups:
            value = request.form.get(f'lead-{g.id}')
            if value is not None:
                g.head_teacher = value.strip() or None
        db.session.commit()
        flash('Руководители сохранены', 'success')
        if request.form.get('go') == 'next':
            return redirect(url_for('steps.step3'))
        return redirect(url_for('steps.step2'))

    counts = dict(db.session.query(Student.group, func.count(Student.id)).group_by(Student.group).all())
    left = sum(1 for g in groups if not (g.head_teacher or '').strip())
    return render_template('admin/steps/step2.html', current=2, groups=groups, counts=counts, left=left)


# ---------- Шаг 3. Сроки ----------

def _date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date() if value else None
    except ValueError:
        return None


@steps.route('/3', methods=['GET', 'POST'])
def step3():
    d = Deadline.current()
    if request.method == 'POST':
        if not d:
            d = Deadline()
            db.session.add(d)
        d.title = request.form.get('title', '').strip() or None
        d.apply_start = _date(request.form.get('apply_start'))
        d.apply_end = _date(request.form.get('apply_end'))
        d.practice_start = _date(request.form.get('practice_start'))
        d.practice_end = _date(request.form.get('practice_end'))

        for a, b, label in ((d.apply_start, d.apply_end, 'набора'),
                            (d.practice_start, d.practice_end, 'практики')):
            if a and b and b < a:
                db.session.rollback()
                flash(f'Дата окончания {label} раньше даты начала', 'danger')
                return redirect(url_for('steps.step3'))

        db.session.commit()
        flash('Сроки сохранены', 'success')
        if request.form.get('go') == 'next':
            return redirect(url_for('steps.step4'))
        return redirect(url_for('steps.step3'))

    return render_template('admin/steps/step3.html', current=3, d=d,
                           apply_preview=state.short_range(d.apply_start, d.apply_end) if d else None,
                           practice_preview=state.short_range(d.practice_start, d.practice_end) if d else None)


# ---------- Шаг 4. Инструкция для своего места (папка app/instruction) ----------

@steps.route('/4', methods=['GET', 'POST'])
def step4():
    if request.method == 'POST':
        state.ensure_dirs()
        if 'text' in request.form:
            state.save_instruction_text(request.form.get('text', '').replace('\r\n', '\n'))
            flash('Инструкция сохранена', 'success')

        saved = 0
        for f in request.files.getlist('files'):
            if not f or not f.filename:
                continue
            name = _safe_name(f.filename)
            ext = os.path.splitext(name or '')[1].lower()
            if not name or ext not in INSTRUCTION_EXTENSIONS or name == state.INSTRUCTION_TEXT_FILE:
                flash(f'Файл «{f.filename}» пропущен: недопустимый формат', 'warning')
                continue
            f.save(os.path.join(current_app.config['INSTRUCTION_PATH'], name))
            saved += 1
        if saved:
            flash(f'Добавлено файлов: {saved}', 'success')

        if request.form.get('go') == 'next':
            return redirect(url_for('steps.step5'))
        return redirect(url_for('steps.step4'))

    return render_template('admin/steps/step4.html', current=4,
                           text=state.instruction_text(), files=state.instruction_files())


@steps.route('/4/files/<path:name>')
def instruction_file(name):
    if name not in {f['name'] for f in state.instruction_files()}:
        abort(404)
    return send_from_directory(current_app.config['INSTRUCTION_PATH'], name, as_attachment=True)


@steps.route('/4/files/<path:name>/delete', methods=['POST'])
def delete_instruction_file(name):
    folder = current_app.config['INSTRUCTION_PATH']
    path = os.path.join(folder, os.path.basename(name))
    if os.path.basename(name) != state.INSTRUCTION_TEXT_FILE and os.path.isfile(path):
        os.remove(path)
        flash('Файл удалён', 'success')
    return redirect(url_for('steps.step4'))


# ---------- Шаг 5. Места практики ----------

@steps.route('/5', methods=['GET', 'POST'])
def step5():
    edit = Place.query.get(request.args.get('edit', type=int)) if request.args.get('edit') else None
    if request.method == 'POST':
        place_id = request.form.get('id', type=int)
        place = Place.query.get_or_404(place_id) if place_id else Place()
        fill_place(place, request.form)
        if not place.title:
            flash('Укажите название предприятия', 'danger')
            return redirect(url_for('steps.step5'))
        if not place_id:
            db.session.add(place)
        db.session.flush()
        state.recount_free_places()
        db.session.commit()
        flash('Место сохранено', 'success')
        return redirect(url_for('steps.step5'))

    places = Place.query.order_by(Place.title).all()
    return render_template('admin/steps/step5.html', current=5, places=places, edit=edit)


@steps.route('/5/<int:id>/delete', methods=['POST'])
def delete_place(id):
    delete_place_record(Place.query.get_or_404(id))
    db.session.commit()
    flash('Место удалено', 'success')
    return redirect(url_for('steps.step5'))


# ---------- Шаг 6. Приложение для студентов (папка static/app) ----------

@steps.route('/6', methods=['GET', 'POST'])
def step6():
    if request.method == 'POST':
        state.ensure_dirs()
        f = request.files.get('apk')
        if f and f.filename:
            name = _safe_name(f.filename)
            if not name or not name.lower().endswith(state.APP_EXTENSIONS):
                flash('Загрузите установочный файл .apk', 'danger')
                return redirect(url_for('steps.step6'))
            folder = current_app.config['APP_PATH']
            for old in os.listdir(folder):
                if old.lower().endswith(state.APP_EXTENSIONS):
                    os.remove(os.path.join(folder, old))
            f.save(os.path.join(folder, name))
            flash('Установочный файл загружен', 'success')
        if 'sent_form' in request.form:
            state.set_app_sent(bool(request.form.get('sent')))
        return redirect(url_for('steps.step6'))

    d = Deadline.current()
    apk = state.app_file()
    until = f' до {d.apply_end:%d.%m}' if d and d.apply_end else ''
    practice = f'«{d.title}»' if d and d.title else 'производственную практику'
    message = (f'Здравствуйте! Набор на {practice} открыт{until}. '
               'Установите приложение «Практика» из прикреплённого файла, '
               'войдите по номеру студенческого билета и выберите место практики.')
    return render_template('admin/steps/step6.html', current=6, apk=apk,
                           message=message, sent=state.app_sent())
