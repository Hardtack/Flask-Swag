from flask import Flask


app = Flask(__name__)


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
def user_read(user_id):
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
