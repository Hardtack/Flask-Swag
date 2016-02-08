from pprint import pprint

from tests.app import app
from flask_swag import core, extractor

pprint(extractor.extract_paths(app))