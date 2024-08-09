#!/usr/bin/python3
"""
This module sets up a Flask route to return a JSON list of all Place objects.
It also allows for GET, POST, PUT, and DELETE requests. and it also searches
for Place objects by state, city, and amenity linked to the Place.
"""
from flask import jsonify, abort, request

from models.user import User
from models.city import City
from models.place import Place
from models import storage

from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id):
    """
    Return a JSON list of all Place objects in a City object with city_id.
    or 404 error if city_id is not linked to any City object.

    Return 200 status code with the list of Place objects
    with City with <city_id> in JSON format if success.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify([
        place.to_dict()
        for place in city.places
    ])


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """
    Return a JSON representation of a Place object
    or 404 error if not found.

    Return 200 status code with the Place object in JSON format if success.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """
    Delete a Place object with place_id or 404 error if not found.

    Return 200 status code with an empty JSON object if success.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def post_place(city_id):
    """
    Create a new Place object in a City object with city_id.

    Return 404 if city_id is not linked to any City object,
    or 400 error if not a JSON, missing user_id or missing name.

    Return 201 status code with the new Place object in JSON format if success.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_data = request.get_json(silent=True)
    if not place_data:
        abort(400, "Not a JSON")
    if "user_id" not in place_data:
        abort(400, "Missing user_id")
    if "name" not in place_data:
        abort(400, "Missing name")

    user = storage.get(User, place_data.get("user_id"))
    if not user:
        abort(404)

    new_place = Place(city_id=city_id, **place_data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place(place_id):
    """
    Update a Place object with place_id. Return 404 if not found.
    Return 400 if not a JSON.

    Return 200 with the updated Place object in JSON format if success.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, "Not a JSON")

    place.update(**place_data)
    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    Search for Place objects based on the JSON in the request.
    Return 400 if not a JSON.

    It filters the Place objects by state, city,
    and amenity linked to the Place.

    The JSON should have the following keys:
    - states: list of state ids to filter by
    - cities: list of city ids to filter by
    - amenities: list of amenity ids to filter by
    If the JSON is empty, return all Place objects.

    Return 200 with a list of Place objects in JSON format if success.
    """
    if request.get_json() is not None:
        params = request.get_json()
        states = params.get('states', [])
        cities = params.get('cities', [])
        amenities = params.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return abort(400, 'Not a JSON')
