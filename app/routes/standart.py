from flask import Blueprint, render_template, request, redirect, jsonify, flash
from flask_login import login_required

from ..models.standart import Standart
from ..extensions import db
from flask import jsonify

standart = Blueprint('standart', __name__)


@standart.route('/standarts', methods=['GET'])
def all():
    standarts = Standart.query.all()
    return render_template('standart/all.html', standarts=standarts)


@standart.route('/standart/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']

        standart = Standart(title=title)

        try:
            db.session.add(standart)
            db.session.commit()
            flash('Успешно добавлено', 'success')
            return redirect('/standart/add')
        except Exception as e:
            print(str(e))
            flash(str(e), 'danger')
            return redirect('/standart/add')
    else:
        return render_template('standart/create.html')


@standart.route('/standarts/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    standart = Standart.query.get(id)
    if request.method == 'POST':
        standart.title = request.form['title']  # Обязательное

        try:
            db.session.commit()
            flash("Запись обновлена", 'success')
            return redirect('/standarts')
        except Exception as e:
            flash(str(e), 'danger')
    else:
        return render_template('standart/update.html', standart=standart)


@standart.route('/standarts/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    standart = Standart.query.get(id)
    try:
        db.session.delete(standart)
        db.session.commit()
        flash('Успех', 'success')
        return redirect('/standarts')
    except Exception as e:
        print(str(e))
        flash(str(e), 'danger')
        return redirect('/standarts')