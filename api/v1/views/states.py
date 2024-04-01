#!/usr/bin/python3
""" define method to handle states query"""
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ retrive states"""
    states = storage.all(State).values()
    if not states:
        abort(404)
    if states:
        state_list = [state.to_dict() for state in states]
        return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """get state by id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ post a state"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        abort(404)
    if 'name' not in data:
        abort(404)
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ update a state"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        abort(404)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if state:
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict()), 200
