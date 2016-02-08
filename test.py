import sys

from tests.app import app
from flask_swag import Swag

swag = Swag(app)

if __name__ == "__main__":
    app.run(debug=True)
