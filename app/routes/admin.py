import io
import os
import re
from datetime import date

from docx import Document
from flask import (Blueprint, render_template, redirect, flash, url_for, request,
                   current_app, send_file, abort)
from flask_login import login_required
from sqlalchemy import func

from ..extensions import db
from ..functions import create_doc
from ..models.student import Student
from ..models.group import Group
from ..models.place import Place
from ..models.review import Review
from ..models.deadline import Deadline
from .. import state
from ..state import OWN_PLACE

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.before_request
@login_required
def _require_login():
    pass


def _int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def place_text(student):
    if student.place == OWN_PLACE and student.title:
        return student.title
    return student.place or ''


# ---------------- Главная ----------------

@admin.route('/')
def dashboard():
    d = Deadline.current()
    students = Student.query.all()
    total = len(students)
    applied = [s for s in students if s.place]
    own = sum(1 for s in applied if s.place == OWN_PLACE)

    group_rows = []
    for g in Group.query.order_by(Group.title).all():
        members = [s for s in students if s.group == g.title]
        done = sum(1 for s in members if s.place)
        group_rows.append({'group': g, 'total': len(members), 'done': done,
                           'left': len(members) - done,
                           'pct': round(done / len(members) * 100) if members else 0})

    places = Place.query.order_by(Place.title).all()

    steps = {s['n']: s['state'] for s in state.steps_state()}
    warnings = []
    if not (d and d.apply_set):
        warnings.append(('Не указан срок набора на практику',
                         'Студенты не увидят, до какого числа можно выбрать место.', 3))
    if not (d and d.practice_set):
        warnings.append(('Не указан срок прохождения практики',
                         'Студенты не увидят даты практики в приложении, а в рапорте будут пустые даты.', 3))
    if steps[2] != 'done' and Group.query.count():
        warnings.append(('Не всем группам назначены руководители',
                         'Руководитель нужен для приложения и рапорта.', 2))
    if steps[6] != 'done':
        warnings.append(('Приложение не отправлено студентам',
                         'Студенты не смогут выбрать место, пока не установят приложение.', 6))

    days_left = None
    if d and d.apply_end:
        days_left = (d.apply_end - date.today()).days

    return render_template('admin/dashboard.html', active='dashboard', deadline=d,
                           total=total, applied=len(applied), own=own,
                           not_applied=total - len(applied),
                           pct=round(len(applied) / total * 100) if total else 0,
                           group_rows=group_rows, places=places, warnings=warnings,
                           days_left=days_left)


# ---------------- Студенты ----------------

@admin.route('/students')
def students():
    students = Student.query.order_by(Student.group, Student.name).all()
    groups = [g[0] for g in db.session.query(Student.group).distinct().order_by(Student.group).all() if g[0]]
    places = [p.title for p in Place.query.order_by(Place.title).all()]
    return render_template('admin/students.html', active='students', students=students,
                           groups=groups, places=places,
                           own_place=OWN_PLACE, place_text=place_text)


def _fill_student(student, form):
    student.student_number = form.get('student_number', '').strip()
    student.name = form.get('name', '').strip()
    student.group = form.get('group', '').strip()
    place = form.get('place', '').strip()
    if place == OWN_PLACE:
        student.title = form.get('title', '').strip() or student.title
    student.place = place or None


@admin.route('/students/add', methods=['POST'])
def add_student():
    student = Student()
    _fill_student(student, request.form)
    if not student.name:
        flash('Укажите ФИО студента', 'danger')
        return redirect(url_for('admin.students'))
    db.session.add(student)
    state.recount_free_places()
    db.session.commit()
    flash('Студент добавлен', 'success')
    return redirect(url_for('admin.students'))


@admin.route('/students/<int:id>/update', methods=['POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    _fill_student(student, request.form)
    state.recount_free_places()
    try:
        db.session.commit()
        flash('Изменения сохранены', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при обновлении студента: {e}', 'danger')
    return redirect(url_for('admin.students', _anchor=f'student-{id}'))


@admin.route('/students/<int:id>/delete', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    state.recount_free_places()
    db.session.commit()
    flash('Студент удалён', 'success')
    return redirect(url_for('admin.students'))


# ---------------- Группы ----------------

@admin.route('/groups')
def groups():
    counts = dict(db.session.query(Student.group, func.count(Student.id)).group_by(Student.group).all())
    done = dict(db.session.query(Student.group, func.count(Student.id))
                .filter(Student.place.isnot(None), Student.place != '').group_by(Student.group).all())
    rows = []
    for g in Group.query.order_by(Group.title).all():
        total = counts.get(g.title, 0)
        d = done.get(g.title, 0)
        rows.append({'group': g, 'total': total, 'done': d, 'pct': round(d / total * 100) if total else 0})
    return render_template('admin/groups.html', active='groups', rows=rows)


def _fill_group(group, form):
    old_title = group.title
    group.title = form.get('title', '').strip()
    group.year = _int(form.get('year'))
    group.head_teacher = form.get('head_teacher', '').strip() or None
    if old_title and old_title != group.title:
        Student.query.filter_by(group=old_title).update({'group': group.title})


@admin.route('/groups/add', methods=['POST'])
def add_group():
    group = Group()
    _fill_group(group, request.form)
    if not group.title:
        flash('Укажите название группы', 'danger')
    else:
        db.session.add(group)
        db.session.commit()
        flash('Группа добавлена', 'success')
    return redirect(url_for('admin.groups'))


@admin.route('/groups/<int:id>/update', methods=['POST'])
def update_group(id):
    group = Group.query.get_or_404(id)
    _fill_group(group, request.form)
    try:
        db.session.commit()
        flash('Изменения сохранены', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при обновлении группы: {e}', 'danger')
    return redirect(url_for('admin.groups'))


@admin.route('/groups/<int:id>/delete', methods=['POST'])
def delete_group(id):
    group = Group.query.get_or_404(id)
    Student.query.filter_by(group=group.title).delete()
    db.session.delete(group)
    state.recount_free_places()
    db.session.commit()
    flash('Группа и её студенты удалены', 'success')
    return redirect(url_for('admin.groups'))


# ---------------- Места практики ----------------

@admin.route('/places')
def places():
    stats = dict((pid, (cnt, avg)) for pid, cnt, avg in
                 db.session.query(Review.id_place, func.count(Review.id), func.avg(Review.rating))
                 .group_by(Review.id_place).all())
    rows = []
    for p in Place.query.order_by(Place.title).all():
        cnt, avg = stats.get(p.id, (0, None))
        rows.append({'place': p, 'reviews': cnt,
                     'rating': f'{avg:.1f}'.replace('.', ',') if avg else '—',
                     'pct': min(100, round(p.taken / p.max_places * 100)) if p.max_places else 0})
    return render_template('admin/places.html', active='places', rows=rows)


def fill_place(place, form):
    old_title = place.title
    place.title = form.get('title', '').strip()
    place.occupation = form.get('occupation', '').strip()
    place.max_places = max(1, _int(form.get('max_places'), 1))
    if 'requirements' in form:
        place.requirements = form.get('requirements', '').strip()
    if 'outlook' in form:
        place.outlook = form.get('outlook', '').strip()
    if 'contacts' in form:
        place.contacts = form.get('contacts', '').strip()
    if old_title and old_title != place.title:
        Student.query.filter_by(place=old_title).update({'place': place.title})
    if place.places is None:
        place.places = place.max_places


def delete_place_record(place):
    Student.query.filter_by(place=place.title).update({'place': None})
    db.session.delete(place)


@admin.route('/places/add', methods=['POST'])
def add_place():
    place = Place()
    fill_place(place, request.form)
    if not place.title:
        flash('Укажите название предприятия', 'danger')
        return redirect(request.referrer or url_for('admin.places'))
    db.session.add(place)
    db.session.flush()
    state.recount_free_places()
    db.session.commit()
    flash('Место добавлено', 'success')
    return redirect(request.referrer or url_for('admin.places'))


@admin.route('/places/<int:id>/update', methods=['POST'])
def update_place(id):
    place = Place.query.get_or_404(id)
    fill_place(place, request.form)
    state.recount_free_places()
    db.session.commit()
    flash('Изменения сохранены', 'success')
    return redirect(request.form.get('next') or url_for('admin.places'))


@admin.route('/places/<int:id>/delete', methods=['POST'])
def delete_place(id):
    delete_place_record(Place.query.get_or_404(id))
    db.session.commit()
    flash('Место удалено', 'success')
    return redirect(request.referrer or url_for('admin.places'))


# ---------------- Отзывы ----------------

@admin.route('/reviews')
def reviews():
    places = Place.query.order_by(Place.title).all()
    counts = dict(db.session.query(Review.id_place, func.count(Review.id)).group_by(Review.id_place).all())
    place_id = request.args.get('place_id', type=int) or (places[0].id if places else None)
    current = Place.query.get(place_id) if place_id else None
    items = (Review.query.filter_by(id_place=place_id).order_by(Review.date.desc()).all()
             if place_id else [])
    ratings = [r.rating for r in items if r.rating is not None]
    avg = f'{sum(ratings) / len(ratings):.1f}'.replace('.', ',') if ratings else '—'
    return render_template('admin/reviews.html', active='reviews', places=places, counts=counts,
                           current=current, reviews=items, avg=avg)


@admin.route('/reviews/<int:id>/delete', methods=['POST'])
def delete_review(id):
    review = Review.query.get_or_404(id)
    place_id = review.id_place
    db.session.delete(review)
    db.session.commit()
    flash('Отзыв удалён', 'success')
    return redirect(url_for('admin.reviews', place_id=place_id))


# ---------------- Рапорт ----------------

@admin.route('/report')
def report():
    d = Deadline.current()
    groups = Group.query.order_by(Group.title).all()
    leads = {g.title: g.head_teacher or '' for g in groups}
    students = [{
        'id': s.id, 'name': s.name or '', 'group': s.group or '',
        'place': place_text(s), 'has_place': bool(s.place), 'lead': leads.get(s.group, ''),
    } for s in Student.query.order_by(Student.group, Student.name).all()]
    duration = ''
    year = ''
    if d and d.practice_set:
        duration = f'{d.practice_start:%d.%m.%Y} – {d.practice_end:%d.%m.%Y}'
        year = str(d.practice_start.year)
    return render_template('admin/report.html', active='report', deadline=d,
                           students=students, groups=[{'title': g.title, 'lead': g.head_teacher or ''} for g in groups],
                           duration=duration, year=year)


@admin.route('/report/docx', methods=['POST'])
def report_docx():
    data = request.get_json(silent=True) or {}
    rows = [(r.get('name', '').strip(), r.get('place', '').strip())
            for r in data.get('rows', []) if r.get('name', '').strip()]
    if not rows:
        return {'success': False, 'message': 'В рапорте нет студентов'}, 400

    year = data.get('year', '')
    group = data.get('group', '')
    duration = data.get('duration', '')
    head_teacher = data.get('head_teacher', '')

    doc = Document(os.path.join(current_app.config['UPLOAD_PATH'], 'template.docx'))
    create_doc(doc, rows, year, group, duration, head_teacher)

    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    safe_group = re.sub(r'[^\w\-, ]+', '', group)[:60] or 'группы'
    return send_file(output, as_attachment=True,
                     download_name=f'Произв.практика_{year}_{safe_group}.docx',
                     mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
