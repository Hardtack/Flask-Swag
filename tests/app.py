from flask import Flask


app = Flask(__name__)

app.config.update({
    'SWAG_TITLE': 'Flask-Swag test application',
    'SWAG_API_VERSION': '0.0.1',
})


@app.route('/')
def main():
    """
    The main page app.
    """
    pass


@app.route('/users/')
def user_index():
    """
    Get list of users.
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
def user_create():
    """
    Create a new user
    """
    pass
