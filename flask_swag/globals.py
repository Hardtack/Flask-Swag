"""
globals
=======

Global variables.

"""
import os

#: Package root directory
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

#: Resources root directory
RESOURCES_DIR = os.path.join(ROOT_DIR, 'resources')

#: Root directory of swagger-ui
SWAGGER_UI_DIR = os.path.join(RESOURCES_DIR, 'swagger-ui', 'dist')
