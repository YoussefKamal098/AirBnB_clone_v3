#!/usr/bin/python3
"""
This module sets up Flask routes for Place objects. It
allows for GET requests to return a JSON list of all Place objects in a City.
"""
from flask import jsonify, request, abort

from models.city import City
from models import storage

from api.v1.views import app_views


@app_views.route("/api/v1/cities/<city_id>/places")
def get_places(city_id):
    """
    Return a JSON list of all Place objects in a City,
    or a 404 error if the City does not exist.
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify([place.to_dict() for place in city.palces])
