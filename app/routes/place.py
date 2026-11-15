from flask import Blueprint, jsonify

from ..models.place import Place

place = Blueprint('place', __name__)


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
