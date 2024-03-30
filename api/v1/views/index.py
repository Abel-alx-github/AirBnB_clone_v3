#!/usr/bin/python3
""" """
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({'status': "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    dic = {}
    dic['amenities'] = storage.count(Amenity)
    dic['cities'] = storage.count(City)
    dic['reviews'] = storage.count(Review)
    dic['states'] = storage.count(State)
    dic['users'] = storage.count(User)

    return jsonify(dic)
