"""
tests.test_extension
====================

Tests for extension

"""
import json

from flask import Flask
from flask_swag import Swag


def test_extension():
    """Basic test for flask extension."""
    app = Flask(__name__)
    app.config['SWAG_TITLE'] = "Test application."
    app.config['SWAG_API_VERSION'] = '1.0.1'

    swag = Swag(app)

    with app.test_request_context('/swagger/swagger.json'):
        swagger_json = app.generate_swagger()

    client = app.test_client()
    response = client.get('/swagger/swagger.json')
    assert 200 == response.status_code
    assert swagger_json == json.loads(response.data.decode('utf-8'))
