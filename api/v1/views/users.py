#!/usr/bin/python3
""" define user class to handle its query"""
from models import storage
from models.user import User

from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_user():
    """ get users"""
    if request.method == 'GET':
        users = storage.all(User)
        users_list = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users_list), 200
    elif request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        if "email" not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """get user by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignor = ["id", "email", "created_at", "updated_at"]
        for k, v in data.items():
            if k not in ignor:
                setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200
