#!/usr/bin/python3
"""defin aminity query methods """

from models.amenity import Amenity
from flask import request, abort, jsonify
from api.v1.views import app_views

from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenity():
    """ get amenities"""
    if request.method == 'GET':
        amenity = storage.all(Amenity)
        amenity_list = []
        for item in amenity.values():
            amenity_list.append(item.to_dict())
        return jsonify(amenity_list), 200
    elif request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        if 'name' not in data:
            abort(400, 'Missing name')
        instance_of_amenity = Amenity(**data)
        instance_of_amenity.save()
        return jsonify(instance_of_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """get aminity by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignor = ['id', "created_at", "updated_at"]
        for k, v in data.items():
            if k not in ignor:
                setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
