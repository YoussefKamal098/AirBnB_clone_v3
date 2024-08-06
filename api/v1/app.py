#!/usr/bin/python3
"""
This module sets up and runs a Flask application for the HBNB API.
"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage"""
    storage.close()


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST')
    PORT = os.getenv('HBNB_API_PORT')

    app.run(
        host=(HOST if HOST else "0.0.0.0"),
        port=(PORT if PORT else 5000),
        threaded=True,
    )
