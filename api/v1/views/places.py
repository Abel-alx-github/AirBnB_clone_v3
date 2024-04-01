#!/usr/bin/python3
""" define method to handle place query"""

from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places_of_city(city_id):
    """ get places"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        places = storage.all(Place).values()
        if places:
            places_list = []
            for place in places:
                if place.city_id == city_id:
                    places_list.append(place.to_dict())
            return jsonify(places_list)
    elif request.method == 'POST':
        if not request.json_get():
            abort(400, 'Not a JSON')
        data = request.get_json()
        if not data:
            abort(400)
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user = storage.get(User, data['user_id'])
        if not user:
            abort(404)
        if 'name' not in data:
            abort(400, 'Missing name')
        data['city_id'] = city_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """ retrive place by its id"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        if not data:
            abort(400)
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        ignor = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in ignor:
                setattr(place, k, v)
        return jsonify(place.to_dict())
