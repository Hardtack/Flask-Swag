"""
flask_swag
==========

Flask extension that extracts swagger spec from flask app & provides
Swagger UI.

"""
from flask import Flask, Blueprint, current_app

from . import core
from .extractor import Extractor


class Swag(object):
    """
    Flask extension class for flask_swag.
    
    This is plain flask extension. So, you can use it like ::
    
        swag = Swag(app)
        
    and also ::
    
        swag = Swag(app)
        
        # Init later
        swag.init_app(app)

    """
    def __init__(self, app: Flask=None, extractor: Extractor=None):
        self.app = app
        self.extractor = extractor or Extractor()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init flask app for Flask-Swag."""
        pass

    def generate_swagger(self, app: Flask=current_app):
        """Generate swagger spec from `app`."""
        return core.Swag(
            version="2.0",
            paths=extractor.extract_paths(app),
        )

    def make_blueprint(self, blueprint_name='swag', prefix=None) -> Blueprint:
        """
        Create a new Swagger UI related blueprint.
        
        :param blueprint_name: name of the blueprint. default is `'swag'`
        :param prefix: URL prefix of the blueprint.
        
        """
        pass

    def register_blueprint(self, app: Flask, blueprint_name='swag', prefix=None) \
            -> Blueprint:
        """
        Register Swagger UI related blueprint.
        
        Registering blueprint is optional.
        So you have to explicitly register blueprint using this method.
        
        :param blueprint_name: name of the blueprint. default is `'swag'`
        :param prefix: URL prefix of the blueprint.
        :returns: created blueprint
        
        """
        blueprint = self.make_blueprint(blueprint_name, prefix)
        app.register_blueprint(blueprint)
        return blueprint