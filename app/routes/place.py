from flask import Blueprint, render_template, request, redirect, jsonify, flash
from flask_login import login_required

from ..models.place import Place
from ..extensions import db
from flask import jsonify

place = Blueprint('place', __name__)


@place.route('/places', methods=['GET'])
def all():
    places = Place.query.all()
    return render_template('place/all.html', places=places)


@place.route('/api/places', methods=['GET'])
def get_places():
    places = Place.query.filter(Place.places > 0).all()
    places_list = []
    for place in places:
        places_list.append({
            "id": place.id,
            "title": place.title,
            "occupation": place.occupation,
            "places": place.places,
            "max_places": place.max_places,
            "requirements": place.requirements,
            "outlook": place.outlook,
            "contacts": place.contacts
        })
    return jsonify(places_list)


@place.route('/place/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']  # Обязательное
        places = request.form['places']  # Обязательное
        requirements = request.form.get('requirements', '')
        occupation = request.form.get('occupation', '')
        outlook = request.form.get('outlook', '')
        contacts = request.form.get('contacts', '')

        place = Place(title=title, places=places, max_places=places, occupation=occupation, requirements=requirements, outlook=outlook, contacts=contacts)

        try:
            db.session.add(place)
            db.session.commit()
            flash('Успешно добавлено', 'success')
            return redirect('/place/add')
        except Exception as e:
            print(str(e))
            flash(str(e), 'danger')
            return redirect('/place/add')
    else:
        return render_template('place/create.html')


@place.route('/places/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    place = Place.query.get(id)
    if request.method == 'POST':
        place.title = request.form['title']  # Обязательное
        place.places = request.form['places']  # Обязательное
        place.max_places = request.form['max_places']  # Обязательное
        place.occupation = request.form.get('occupation', '')
        place.requirements = request.form.get('requirements', '')
        place.outlook = request.form.get('outlook', '')
        place.contacts = request.form.get('contacts', '')

        try:
            db.session.commit()
            return redirect('/places')
        except Exception as e:
            print(str(e))
    else:
        return render_template('place/update.html', place=place)


@place.route('/places/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    place = Place.query.get(id)
    try:
        db.session.delete(place)
        db.session.commit()
        flash('Успех', 'success')
        return redirect('/places')
    except Exception as e:
        print(str(e))
        flash('Запись не была удалена', 'danger')
        return redirect('/places')