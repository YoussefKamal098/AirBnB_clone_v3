#!/usr/bin/python3
"""
This module sets up a Flask route to return a JSON list of all State objects.
"""
from flask import jsonify, abort, request

from models import storage
from models.state import State

from api.v1.views import app_views


@app_views.route("/states/", methods=["GET"])
def get_states():
    """Return a JSON list of all State objects"""
    return jsonify([
        state.to_dict()
        for state in storage.all(State).values()
    ])


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Return a JSON representation of a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"])
def post_state():
    """Create a new State object"""
    state_data = request.get_json()

    if not state_data:
        abort(400, "Not a JSON")
    if "name" not in state_data:
        abort(400, "Missing name")

    new_state = State(name=state_data.get("name"))
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    '''Updates a State object'''
    all_states = storage.all(State).values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
