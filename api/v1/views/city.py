#!/usr/bin/python3

from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities_of_state(state_id):
    citys = storage.all(City)
    if not citys:
        abort(404)
    if citys:
        city_list = []
        for city in citys.values():
            if state_id == city.state_id:
                city_list.append(city.to_dict())
        return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_del_city_by_id(city_id):
    city = storage.get(City, city_id)
    if request.method == 'GET':
        if city:
            return jsonify(city.to_dict()), 200
        abort(404)
    elif request.method == 'DELETE':
        if city:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(404, description='NOT a JSON')
    if 'name' not in data:
        abort(404, description='Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_or_update(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(404, 'Not a JSON')
    ignore = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
