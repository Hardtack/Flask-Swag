"""
tests.test_extractor
====================

Tests for extractor.

"""
from flask import Flask, Blueprint

from flask_swag.extractor import Extractor


def test_extractor():
    """Basic test for extractor"""
    # Define flask app
    app = Flask(__name__)

    @app.route('/users/')
    def index():
        """Get list of users."""
        pass

    @app.route('/users/', methods=['POST'])
    def create():
        """Create a new user."""
        pass

    @app.route('/users/<int:user_id>')
    def read(user_id):
        """Read user's info."""
        pass

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete(user_id: int):
        """Delete a user."""
        pass

    # Create a extractor
    extractor = Extractor()

    paths = extractor.extract_paths(app,
                                    exclude_endpoint=['static'])

    full_expected = {
        '/users/': {
            'get': {
                'description': "Get list of users.",
                'summary': "Get list of users.",
                'parameters': [],
                'responses': {'default': {'description': ''}},
            },
            'post': {
                'description': "Create a new user.",
                'summary': "Create a new user.",
                'parameters': [],
                'responses': {'default': {'description': ''}},
            },
        },
        '/users/{user_id}': {
            'get': {
                'description': "Read user's info.",
                'summary': "Read user's info.",
                'parameters': [
                    {
                        'name': 'user_id',
                        'in_': 'path',
                        'type': 'number',
                        'format': 'integer',
                        'required': True,
                    },
                ],
                'responses': {'default': {'description': ''}},
            },
            'delete': {
                'summary': "Delete a user.",
                'description': "Delete a user.",
                'parameters': [
                    {
                        'name': 'user_id',
                        'in_': 'path',
                        'type': 'number',
                        'format': 'integer',
                        'required': True,
                    },
                ],
                'responses': {'default': {'description': ''}},
            },
        },
    }
    assert full_expected == paths

    # Extract 'read' only.
    paths = extractor.extract_paths(app,
                                    endpoint='read')
    assert {
        '/users/{user_id}': {
            'get': full_expected['/users/{user_id}']['get']
        },
    } == paths

    # Extract 'create' & 'read'
    paths = extractor.extract_paths(app,
                                    endpoint=['read', 'create'])
    assert {
        '/users/': {
            'post': full_expected['/users/']['post']
        },
        '/users/{user_id}': {
            'get': full_expected['/users/{user_id}']['get']
        },
    } == paths


def test_blueprint():
    """Basic test for extractor"""
    # Define flask app
    app = Flask(__name__)

    @app.route('/users/<int:user_id>')
    def read(user_id):
        """Read user's info."""
        pass

    # Define blueprint
    blueprint = Blueprint('post', __name__)

    @blueprint.route('/posts/')
    def index():
        """Get list of posts."""
        pass

    # Register
    app.register_blueprint(blueprint, url_prefix='/blueprints')

    # Create a extractor
    extractor = Extractor()

    paths = extractor.extract_paths(app,
                                    exclude_endpoint=['static'])

    full_expected = {
        '/users/{user_id}': {
            'get': {
                'description': "Read user's info.",
                'summary': "Read user's info.",
                'parameters': [
                    {
                        'name': 'user_id',
                        'in_': 'path',
                        'type': 'number',
                        'format': 'integer',
                        'required': True,
                    },
                ],
                'responses': {'default': {'description': ''}},
            },
        },
        '/blueprints/posts/': {
            'get': {
                'description': "Get list of posts.",
                'summary': "Get list of posts.",
                'parameters': [],
                'responses': {'default': {'description': ''}},
            },
        },
    }
    assert full_expected == paths

    # Extract blueprint only.
    paths = extractor.extract_paths(app, blueprint='post')
    assert {
        '/blueprints/posts/': {
            'get': full_expected['/blueprints/posts/']['get'],
        },
    } == paths

    # Extract non-blueprint only.
    paths = extractor.extract_paths(app, blueprint=None,
                                    exclude_endpoint='static')
    assert {
        '/users/{user_id}': {
            'get': {
                'description': "Read user's info.",
                'summary': "Read user's info.",
                'parameters': [
                    {
                        'name': 'user_id',
                        'in_': 'path',
                        'type': 'number',
                        'format': 'integer',
                        'required': True,
                    },
                ],
                'responses': {'default': {'description': ''}},
            },
        },
    } == paths
