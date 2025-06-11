import csv
import io
from datetime import datetime
import os
import secrets
import time
from flask import request, send_file
import zipfile
from fileinput import filename

from flask import current_app, jsonify, send_from_directory
from PIL import Image, UnidentifiedImageError

from flask import Blueprint, render_template, request, redirect, jsonify, flash
from flask_login import login_required, current_user
from flask_wtf import file
from sqlalchemy import text
from sqlalchemy import desc, or_

from ..models.user import User
from ..models.intern import Intern
from ..models.student import Student
from ..models.group import Group
from ..models.place import Place
from ..extensions import db

intern = Blueprint('intern', __name__)

# Сайт

def get_filtered_interns(filter_param):
    interns = Intern.query.filter_by(head_teacher=current_user.name)

    if filter_param == 'none':
        return interns.filter(
            or_(
                Intern.status == 'Без заявки',
                Intern.status == 'Выбор кафедры'
            )
        ).order_by(desc(Intern.score)).all()

    elif filter_param == 'pending':
        pending_interns = interns.filter_by(status='Ожидает подтверждения').order_by(desc(Intern.score)).all()
        updated = False
        result = []

        for intern in pending_interns:
            if intern.place != 'Свое место практики':
                place = Place.query.filter(Place.title.ilike(intern.place)).first_or_404()
                if place.places <= 0:
                    intern.status = 'Без заявки'
                    intern.message = 'Мест не осталось. Выберите другое предприятие...'
                    updated = True
                else:
                    result.append(intern)
            else:
                result.append(intern)

        if updated:
            db.session.commit()

        return result

    elif filter_param == 'confirmed':
        return interns.filter_by(status='Подтвержден').order_by(desc(Intern.score)).all()

    else:
        return interns.order_by(desc(Intern.score)).all()


@intern.route('/intern/all', methods=['GET'])
def all():
    start = time.time()
    if current_user.practice_deadline is not None:
        if datetime.utcnow() > current_user.practice_deadline:
            for intern in Intern.query.filter_by(head_teacher=current_user.name).filter_by(status='Без заявки').all():
                intern.status = 'Выбор кафедры'
            db.session.commit()
    filter_param = request.args.get('filter', 'pending')
    interns = get_filtered_interns(filter_param)
    end = time.time()
    print(f"/intern-table took {round((end - start) * 1000)} ms")
    return render_template('intern/all.html', interns=interns, current_filter=filter_param)


@intern.route('/intern/<int:id>/force', methods=['GET', 'POST'])
def force(id):
    intern = Intern.query.get_or_404(id)
    places = [p[0] for p in db.session.query(Place.title).filter(Place.places > 0).all()]
    places.append('Свое место практики')
    if request.method == 'POST':
        if request.form.get('name') != intern.name:
            intern.name = request.form.get('name')
        if request.form.get('group') != intern.group:
            intern.group = request.form.get('group')
        if request.form.get('year') != intern.year:
            intern.year = request.form.get('year')
        if request.form.get('head_teacher') != intern.head_teacher:
            intern.head_teacher = request.form.get('head_teacher')
        if request.form.get('score') != intern.score:
            intern.score = request.form.get('score')

        intern.place = request.form['place']
        intern.status = 'Подтвержден'
        try:
            db.session.commit()
        except Exception as e:
            flash(str(e), 'danger')
            print(str(e))
            return redirect('/intern/all')

        return redirect('/intern/all')
    else:
        return render_template('intern/force_place.html', intern=intern, places=places)


@intern.route('/intern/<int:id>/update', methods=['POST'])
@login_required
def upgrade_status(id):
    intern = Intern.query.get_or_404(id)
    intern.status = "Подтвержден"

    if intern.place != 'Свое место практики':
        place = Place.query.filter(Place.title.ilike(intern.place)).first_or_404()
        if place.places > 0:
            place.places -= 1
        else:
            flash('Нет свободных мест', 'danger')
            intern.status = 'Без заявки'
            intern.message = 'Мест не осталось. Выберите другое предприятие...'
            db.session.commit()
            return redirect('intern/all')

    try:
        db.session.commit()
        return redirect('/intern/all')
    except Exception as e:
        flash(str(e), 'danger')
        print(str(e))
        return redirect('/intern/all')


@intern.route('/intern/<int:id>/cancel', methods=['POST'])
@login_required
def downgrade_status(id):
    intern = Intern.query.get_or_404(id)
    intern.status = "Без заявки"

    if intern.place != 'Свое место практики':
        place = Place.query.filter_by(title=intern.place).first_or_404()
        place.places = place.places + 1
    else:
        if intern.letter:
            try:
                file_path = os.path.join(current_app.config['SERVER_PATH'], intern.letter)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                flash(e, 'danger')
                print(f"Ошибка при удалении файла: {e}")

        intern.letter = ''

    try:
        db.session.commit()
        return redirect('/intern/all')
    except Exception as e:
        flash(str(e), 'danger')
        print(str(e))
        return redirect('/intern/all')
    

@intern.route('/intern/letter/download/<filename>', methods=['POST', 'GET'])
def download_letter(filename):
    full_path = os.path.join(current_app.config['SERVER_PATH'], filename)
    print(f"[DEBUG] Пытаемся скачать: {full_path}")
    if not os.path.exists(full_path):
        print("[DEBUG] Файл не найден")

    return send_from_directory(
        current_app.config['SERVER_PATH'],
        filename,
        as_attachment=True
    )

@intern.route('/intern/letter/delete', methods=['POST', 'GET'])
def clear_uploads_folder():
    folder = current_app.config['SERVER_PATH']

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            flash(str(e), 'danger')
            print(f"Ошибка при удалении файла {file_path}: {e}")
            return redirect('/intern/all')

    flash('Письма удалены', 'success')
    return redirect('/intern/all')


@intern.route('/download-uploads')
def download_uploads():
    uploads_dir = current_app.config['SERVER_PATH']

    # Проверим, что папка существует
    if not os.path.exists(uploads_dir):
        return "Папка uploads не найдена.", 404

    # Создаем архив в оперативной памяти
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(uploads_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, uploads_dir)
                zip_file.write(file_path, arcname)

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='uploads.zip'
    )

@intern.route('/intern/upload', methods=['GET'])
def upload_interns():
    group = Group.query.filter_by(head_teacher=current_user.name).first()
    print(current_user.name)
    if group:
        # Очистка таблицы
        db.session.query(Intern).delete()
        db.session.execute(text("ALTER SEQUENCE intern_id_seq RESTART WITH 1"))

        students = Student.query.filter_by(group=group.title).all()

        for student in students:
            intern = Intern(
                student_id=student.id,
                name = student.name,
                group = student.group,
                year = group.year,
                head_teacher = current_user.name,
                score = student.score,
                status = 'Без заявки'
            )
            db.session.add(intern)

        try:
            db.session.commit()
            flash('Данные успешно загружены', 'success')
            return redirect('/intern/all')
        except Exception as e:
            flash(str(e), 'danger')
            return redirect('/intern/all')

    else:
        flash('Руководитель практики еще не назначен', 'danger')
        return redirect('/intern/all')

# API для приложения

@intern.route('/intern/get', methods=['GET', 'POST'])
def get_intern():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400
    intern_id = data.get('intern_id')
    intern = Intern.query.get(intern_id)
    place = Place.query.filter_by(title=intern.place).first()
    user = User.query.filter_by(name=intern.head_teacher).first()
    if intern and user:
        return jsonify({
            "success": True,
            "status": intern.status,
            "deadline": user.practice_deadline,
            "place": intern.place if intern.place else None,
            "place_id": place.id if place else None
        }), 200
    else:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401


@intern.route('/intern/post', methods=['GET', 'POST'])
def post_intern():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400
    intern_id = data.get('intern_id')
    place_id = data.get('place_id')

    intern = Intern.query.get(intern_id)
    place = Place.query.get(place_id)
    intern.place = place.title
    intern.status = 'Ожидает подтверждения'
    db.session.commit()

    user = User.query.filter_by(name=intern.head_teacher).first()
    if intern and user:
        return jsonify({
            "success": True,
            "status": intern.status,
            "deadline": user.practice_deadline
        }), 200
    else:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 401


@intern.route('/intern/letter', methods=['GET', 'POST'])
def get_letter():
    if 'id' not in request.form:
        return jsonify({"success": False, "message": "Missing id"}), 401
    try:
        intern_id = int(request.form['id'])
    except ValueError:
        return jsonify({"success": False, "message": "Invalid id"}), 400

    if 'image' not in request.files:
        return jsonify({"success": False, "message": "Missing image file"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400

    return save_letter(intern_id, file)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_letter(intern_id, picture):
    try:
        i = Image.open(picture)
        i.verify()
        picture.seek(0)

        if allowed_file(picture.filename):
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(picture.filename)
            picture_fn = random_hex + f_ext
            picture_path = os.path.join(current_app.config['SERVER_PATH'], picture_fn)

            i = Image.open(picture)
            i.save(picture_path)

            intern = Intern.query.filter_by(id=intern_id).first()
            intern.letter = picture_fn
            intern.place = 'Свое место практики'
            intern.status = 'Ожидает подтверждения'
            db.session.commit()

            print(picture_path)
            return jsonify({"success": True, "message": "Письмо получено"}), 200
        else:
            return jsonify({"success": False, "message": "Invalid file"}), 400
    except UnidentifiedImageError:
        return jsonify({"success": False, "message": "Invalid file"}), 400