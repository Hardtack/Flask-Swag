import os
import sys
from flask_swag import Swag
from tests.app import app

#sys.path.append(os.path.abspath(os.path.join('..', 'meety-server')))
#from meety.app import create_app


#app = create_app(os.path.abspath(
#    os.path.join('..', 'meety-server', 'configurations', 'local.py')
#))

#app.config.update({
#    'SWAG_TITLE': "Meety REST API Server.",
#    'SWAG_API_VERSION': "0.1.0",
#})

swag = Swag(app)

if __name__ == "__main__":
    app.run(debug=True)
