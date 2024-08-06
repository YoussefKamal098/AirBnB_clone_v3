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
    try:
        return jsonify([
            state.to_dict()
            for state in storage.all(State).values()
        ])
    except Exception as err:
        abort(500, f"{err.args[0]}")


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Return a JSON representation of a State object"""
    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        return jsonify(state.to_dict())
    except Exception as err:
        abort(500, f"{err.args[0]}")


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete a State object"""
    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        state.delete()
        storage.save()

        return jsonify({}), 200
    except Exception as err:
        abort(500, f"{err.args[0]}")


@app_views.route("/states/", methods=["POST"])
def post_state():
    """Create a new State object"""
    state_data = request.get_json()

    if not state_data:
        abort(400, "Not a JSON")
    if "name" not in state_data:
        abort(400, "Missing name")

    try:
        new_state = State(name=state_data.get("name"))
        new_state.save()

        return jsonify(new_state.to_dict()), 201
    except Exception as err:
        abort(500, f"{err.args[0]}")


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """Update a State object"""
    try:
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        update_data = request.get_json()
        if not update_data:
            abort(400, "Not a JSON")

        state.name = update_data.get("name", state.name)
        state.save()

        return jsonify(state.to_dict()), 200

    except Exception as err:
        abort(500, f"{err.args[0]}")
