#!/usr/bin/python3
""" defines methods to handl query to place_review"""

from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_place_review(place_id):
    """ get and put """
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        reviews = storage.all(Review).values()
        if reviews:
            reviews_list = [review.to_dict() for review in reviews
                            if review.place_id == place_id]
            return jsonify(reviews_list), 200
    elif request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        if not data:
            abort(404)
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user = storage.get(User, data['user_id'])
        if not user:
            abort(404)
        if 'text' not in data:
            abort(400, 'Missing text')
        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """ get, delete, put"""
    if request.method == 'GET':
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        return jsonify(review.to_dict()), 200
    elif request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        if not data:
            abort(400)
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        ignor = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in ignor:
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200
