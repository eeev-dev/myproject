import os
from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user, current_user

from ..functions import create_doc
from ..models.intern import Intern
from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
from ..models.user import User

from flask import send_file
from docx import Document
from io import BytesIO

user = Blueprint('user', __name__)


@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data, login=form.login.data, password=hashed_password)
            try:
                db.session.add(user)
                db.session.commit()
                flash(f"Поздравляем, {form.login.data}! Вы успешно зарегистрировались", "success")
                return redirect('/')
            except Exception as e:
                print(str(e))
                flash("При регистрации произошла ошибка", "danger")
        else:
            flash(str(form.errors), "danger")
            return redirect(url_for('post.all'))

    return render_template('user/register.html', form=form)


@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Вы успешно авторизовались", "success")
            return redirect(next_page) if next_page else redirect(url_for('user.login'))
        else:
            flash(str(form.errors), "danger")
    return render_template('user/login.html', form=form)


@user.route('/user/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/user/login')


@user.route('/user/deadline', methods=['GET', 'POST'])
def set_deadline():
    if request.method == 'POST':
        dt_str = request.form['deadline']  # формат: '2025-05-20T14:30'
        current_user.practice_deadline = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
        db.session.commit()
        return redirect(url_for('intern.all'))  # или другой нужный маршрут
    else:
        return render_template('user/set_deadline.html', value=current_user.practice_deadline)

@user.route('/user/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        filter_year = int(request.form['filter_year'])
        year = request.form['year']
        group = request.form['group']
        duration = request.form['duration']
        head_teacher = current_user.name

        interns = (Intern.query
                   .filter_by(head_teacher=head_teacher)
                   .filter_by(year=filter_year)
                   .filter_by(group=group)
                   .filter_by(status='Подтвержден')
                   .all())

        doc = Document('app/static/files/template.docx')

        create_doc(doc, interns)

        output = BytesIO()
        doc.save(output)
        output.seek(0)

        return send_file(output,
                         as_attachment=True,
                         download_name=f'Произв.практика_{year}_{group}.docx',
                         mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    else:
        return render_template('user/report.html')