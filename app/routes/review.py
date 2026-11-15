from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload

from ..api_errors import ApiError, payload
from ..extensions import db
from ..models.place import Place
from ..models.review import Review

review = Blueprint('review', __name__)


def _place_id(value, required):
    if value in (None, ''):
        if required:
            raise ApiError("Не указано место практики (place_id)", 400)
        return None
    try:
        place_id = int(value)
    except (TypeError, ValueError):
        raise ApiError("Некорректный place_id", 400)
    if not Place.query.get(place_id):
        raise ApiError("Место практики не найдено", 404)
    return place_id


def _parse_date(value):
    if not value:
        return datetime.now()
    value = str(value).strip()
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        pass
    for fmt in ('%d.%m.%Y %H:%M:%S', '%d.%m.%Y %H:%M', '%d.%m.%Y'):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ApiError("Некорректная дата отзыва", 400)


@review.route('/api/reviews', methods=['GET', 'POST'])
def get_reviews():
    # place_id необязателен: без него возвращаются все отзывы
    data = request.get_json(silent=True)
    if data is not None and not isinstance(data, dict):
        raise ApiError("Тело запроса должно быть JSON-объектом", 400)
    place_id = _place_id((data or {}).get('place_id'), required=False)

    query = Review.query.options(joinedload(Review.place))
    if place_id:
        query = query.filter(Review.id_place == place_id)

    return jsonify([{
        "id": r.id,
        "rating": r.rating,
        "text": r.text,
        "date": r.date,
        "id_place": r.id_place
    } for r in query.all()])


@review.route('/review/post', methods=['GET', 'POST'])
def post_review():
    data = payload()
    place_id = _place_id(data.get('place_id'), required=True)

    try:
        rating = int(data.get('rating'))
    except (TypeError, ValueError):
        raise ApiError("Укажите оценку", 400)
    if not 1 <= rating <= 5:
        raise ApiError("Оценка должна быть от 1 до 5", 400)

    text = str(data.get('text') or '').strip()
    if not text:
        raise ApiError("Напишите текст отзыва", 400)

    date = _parse_date(data.get('date'))

    db.session.add(Review(id_place=place_id, rating=rating, text=text, date=date))
    db.session.commit()
    return jsonify({"success": True, "message": "Отзыв сохранён"}), 200
