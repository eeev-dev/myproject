from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user, current_user

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

        doc = Document('static/files/template.docx')

        # Замена плейсхолдеров в параграфах с учетом разбиения на run-ы
        def replace_placeholder_in_paragraphs(doc, placeholder, new_text):
            for p in doc.paragraphs:
                if placeholder in p.text:
                    # Собираем полный текст абзаца
                    full_text = ''.join(run.text for run in p.runs)
                    if placeholder in full_text:
                        new_full_text = full_text.replace(placeholder, new_text)
                        # очищаем все run-ы
                        for run in p.runs:
                            run.text = ''
                        # вставляем новый текст в первый run
                        if p.runs:
                            p.runs[0].text = new_full_text
                        else:
                            p.add_run(new_full_text)

        replace_placeholder_in_paragraphs(doc, '{{YEAR}}', str(year))
        replace_placeholder_in_paragraphs(doc, '{{HEAD_TEACHER}}', head_teacher)
        replace_placeholder_in_paragraphs(doc, '{{GROUP}}', str(group))
        replace_placeholder_in_paragraphs(doc, '{{DURATION}}', duration)

        # Функция замены плейсхолдера {{TABLE}} таблицей
        def replace_placeholder_with_table(doc, placeholder, data):
            for paragraph in doc.paragraphs:
                if placeholder in paragraph.text:
                    p = paragraph._element
                    parent = p.getparent()
                    parent.remove(p)  # удаляем параграф с плейсхолдером

                    # Добавляем таблицу в конец документа
                    table = doc.add_table(rows=1, cols=len(data[0]))
                    hdr_cells = table.rows[0].cells
                    for j, val in enumerate(data[0]):
                        hdr_cells[j].text = val

                    for row_data in data[1:]:
                        row_cells = table.add_row().cells
                        for k, val in enumerate(row_data):
                            row_cells[k].text = val

                    break

        table_data = [('№', 'Студенттердин ААА', 'Мекемелердин аты')]
        for idx, intern in enumerate(interns, start=1):
            table_data.append((str(idx), intern.name, intern.place))

        replace_placeholder_with_table(doc, '{{TABLE}}', table_data)

        output = BytesIO()
        doc.save(output)
        output.seek(0)

        return send_file(output,
                         as_attachment=True,
                         download_name=f'report_{year}_{group}.docx',
                         mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    else:
        return render_template('user/report.html')