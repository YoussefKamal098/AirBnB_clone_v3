#!/usr/bin/python3
"""
This module sets up a Flask route to return the status of the application.
"""

from flask import jsonify

from models import storage
from models.engine.stored_classes import CLASSES

from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """ routes to status page """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """ retrieves the number of each objects by type """
    return jsonify({f'{key[0].lower() + key[1:]}s': storage.count(value) for key, value in CLASSES.items()})
