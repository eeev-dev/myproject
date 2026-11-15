from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from ..forms import LoginForm
from ..models.admin import AdminUser
from .. import state

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    return redirect(url_for('admin.dashboard'))


@auth.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        if AdminUser.check(form.login.data, form.password.data):
            login_user(AdminUser(), remember=form.remember.data)
            next_page = request.args.get('next')
            dashboard = url_for('admin.dashboard')
            # Конкретную страницу из ?next= открываем как есть,
            # а вместо главной — первый незавершённый шаг настройки
            if next_page and next_page.startswith('/') and not next_page.startswith('//') \
                    and next_page != dashboard:
                return redirect(next_page)
            if any(s['state'] != 'done' for s in state.steps_state()):
                return redirect(url_for('steps.index'))
            return redirect(dashboard)
        flash('Неверный логин или пароль', 'danger')
    return render_template('admin/login.html', form=form)


@auth.route('/admin/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
