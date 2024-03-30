#!/usr/bin/python3
""" """
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    states = storage.all('State')
    state_list = [state.to_dict() for state in states.values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    states = storage.all('State')
    for state in states.values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state:
        print('deleting')
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    if not request.get_json:
        abort(404)
    data = request.get_json()
    if 'name' in data:
        state = State(**data)
        state.save()
        return make_response(jsonify(state.to_dict()), 201)
    abort(404, 'Missing name')


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    if not request.get_json:
        abort(404, 'Not a JSON')
    data = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if state:
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
