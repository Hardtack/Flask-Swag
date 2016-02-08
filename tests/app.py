from flask import Flask
from flask_swag.mark import Mark

mark = Mark()


app = Flask(__name__)

app.config.update({
    'SWAG_TITLE': 'Flask-Swag test application',
    'SWAG_API_VERSION': '0.0.1',
})


@app.route('/')
@mark.summary("Main page")
def main():
    """
    The main page of app.
    """
    pass


@app.route('/users/')
@mark.query('page', int, optional=True)
def user_index():
    """
    Get paginated list of users.
    """
    pass


@app.route('/users/<int:user_id>')
def user_read(user_id: int):
    """
    Read user's info.
    """
    pass


@app.route('/users/', methods=['POST'])
@app.route('/users/create', methods=['GET', 'POST'])
@mark.schema({
    'properties': {
        'description': {'type': 'string'},
        'name': {'type': 'string'},
    },
    'required': ['name'],
    'type': 'object',
})
@mark.response(201, {
    'description': "Created User.",
    'schema': {
        'properties': {
            'description': {'type': 'string'},
            'name': {'type': 'string'},
            'id': {'type': 'integer'},
        },
        'type': 'object',
    },
})
@mark.response(400, "Wrong form data", {
    'properties': {'error': {'type': 'string'}},
    'type': 'object',
})
def user_create():
    """
    Create a new user
    """
    pass
