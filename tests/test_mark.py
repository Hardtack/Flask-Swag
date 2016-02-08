"""
tests.test_extractor
====================

Tests for mark.

"""
from flask import Flask, Blueprint

from flask_swag.extractor import MarkExtractor
from flask_swag.mark import Mark


def test_mark():
    """Basic test for mark"""
    # Create a mark
    mark = Mark()

    # Define flask app
    app = Flask(__name__)

    user_schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
        }
    }

    user_list_schema = {
        'type': 'array',
        'items': user_schema.copy(),
    }

    user_create_schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
        },
        'required': ['name'],
    }

    @app.route('/users/')
    @mark.summary("User index.")
    @mark.query('page', int, optional=True)
    @mark.response(200, {'description': "List of users.",
                         'schema': user_list_schema})
    def index():
        """Get list of users."""
        pass

    @app.route('/users/', methods=['POST'])
    @mark.schema(user_create_schema)
    @mark.response(201, "Created user.", user_schema)
    def create():
        """Create a new user."""
        pass

    assert {
        'summary': "User index.",
        'parameters': [{
            'name': 'page',
            'type': 'number',
            'format': 'integer',
            'in_': 'query',
            'required': False,
        }],
        'responses': {
            200: {
                'description': "List of users.",
                'schema': user_list_schema
            },
        },
    } == mark.get_swag(index)

    # Create an extractor
    extractor = MarkExtractor()

    assert {
        '/users/': {
            'post': {
                'summary': "Create a new user.",
                'description': "Create a new user.",
                'parameters': [{
                    'name': 'name',
                    'type': 'string',
                    'in_': 'formData',
                    'required': True,
                }, {
                    'name': 'description',
                    'type': 'string',
                    'in_': 'formData',
                    'required': False,
                }],
                'responses': {
                    201: {
                        'description': "Created user.",
                        'schema': user_schema
                    },
                }
            }
        }
    } == extractor.extract_paths(app, endpoint='create')
