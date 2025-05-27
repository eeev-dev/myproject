from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.orm import joinedload

from ..models.place import Place
from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
from ..models.review import Review

review = Blueprint('review', __name__)

@review.route('/reviews', methods=['GET'])
def all():
    place_id = request.args.get('place_id', type=int)
    places = Place.query.all()

    query = Review.query.options(joinedload(Review.place))
    if place_id:
        query = query.filter(Review.id_place == place_id)

    reviews = query.all()
    return render_template('review/all.html', reviews=reviews, places=places)


@review.route('/reviews/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    review = Review.query.get(id)
    try:
        db.session.delete(review)
        db.session.commit()
        return redirect('/reviews')
    except Exception as e:
        print(str(e))
        flash(str(e), 'danger')
        return redirect('/reviews')


@review.route('/api/reviews', methods=['GET', 'POST'])
def get_reviews():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400

    place_id = data.get('place_id')
    query = Review.query.options(joinedload(Review.place))
    if place_id:
        query = query.filter(Review.id_place == place_id)

    reviews = query.all()
    reviews_list = []
    for review in reviews:
        reviews_list.append({
            "id": review.id,
            "rating": review.rating,
            "text": review.text,
            "date": review.date,
            "id_place": review.id_place
        })
    return jsonify(reviews_list)


@review.route('/review/post', methods=['GET', 'POST'])
def post_review():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Нет данных в теле запроса"}), 400
    rating = data.get('rating')
    text = data.get('text')
    date = data.get('date')
    place_id = data.get('place_id')

    try:
        review = Review(id_place=place_id, rating=rating, text=text, date=date)
        db.session.add(review)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Отзыв сохранен"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Ошибка добавления"}), 401