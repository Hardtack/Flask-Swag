"""
flask_swag
==========

Flask extension that extracts swagger spec from flask app & provides
Swagger UI.

"""
import os

from flask import Flask, Blueprint, current_app, jsonify, send_from_directory, \
    url_for

from . import core
from .extractor import Extractor
from .globals import SWAGGER_UI_DIR


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
    def __init__(self, app: Flask=None, extractor: Extractor=None,
                 *args, **kwargs):
        """
        :param app: app to be initialized
        :param extractor: extractor instance, default is
                          :class:`.extractor.Extractor`
        :param \*args: args to be passed to :meth:`init_app`
        :param \*\*kwargs: kwargs to be passed to :meth:`init_app`
        """
        self.app = app
        self.extractor = extractor or Extractor()
        if app is not None:
            self.init_app(app, *args, **kwargs)

    def init_app(self, app, blueprint_name='swag', prefix='/swagger',
                 swagger_ui_root=SWAGGER_UI_DIR):
        """Init flask app for Flask-Swag."""
        app.swagger = self.generate_swagger(app)
        self.register_blueprint(app,
                                blueprint_name=blueprint_name,
                                   prefix=prefix,
                                swagger_ui_root=swagger_ui_root)

    def generate_swagger(self, app: Flask=current_app):
        """Generate swagger spec from `app`."""
        return core.convert(core.Swagger(
            version="2.0",
            paths=self.extractor.extract_paths(app),
            info=core.Info(
                title="TODO: Fix me title",
                version="0.0.1",
            )
        ))

    def make_blueprint(self, blueprint_name='swag', 
                       swagger_ui_root=SWAGGER_UI_DIR) -> Blueprint:
        """
        Create a new Swagger UI related blueprint.
        
        :param blueprint_name: name of the blueprint. default is `'swag'`
        :param prefix: URL prefix of the blueprint.
        
        """
        blueprint = Blueprint(blueprint_name, __name__)
        
        @blueprint.route('/swagger.json')
        def swagger_json():
            return jsonify(current_app.swagger)
        
        @blueprint.route('/ui/<path:path>')
        def swagger_ui(path):
            return send_from_directory(swagger_ui_root, path,
                                       cache_timeout=3600)
        
        @blueprint.route('/ui/')
        def swagger_ui_index():
            with open(os.path.join(swagger_ui_root, 'index.html')) as f:
                content = f.read()
            # Inject javascript code
            url = url_for('{}.{}'.format(blueprint_name, 'swagger_json'))
            js = """
                  $(function() {{
                    window.swaggerUi.updateSwaggerUi({{
                        url: '{url}',
                         apiKey: ''
                    }});
                }});
            """.format(url=url)
            tag = '<script type="text/javascript">{js}</script>'.format(
                js=js
            )
            components = content.rsplit('</body>', 1)
            if len(components) == 1:
                content, = components
                components = content.rsplit('</html>', 1)
                if len(components) == 1:
                    html = content + tag
                else:
                    first, rest = components
                    html = first + tag + '</html>' + rest
            else:
                first, rest = components
                html = first + tag + '</body>' + rest
            
            return html, 200
        return blueprint

    def register_blueprint(self, app: Flask, blueprint_name='swag', prefix='/swagger',
                           swagger_ui_root=SWAGGER_UI_DIR) \
            -> Blueprint:
        """
        Register Swagger UI related blueprint.
        
        :param blueprint_name: name of the blueprint. default is `'swag'`
        :param prefix: URL prefix of the blueprint.
        :returns: created blueprint
        
        """
        blueprint = self.make_blueprint(blueprint_name, swagger_ui_root)
        app.register_blueprint(blueprint, url_prefix=prefix)
        return blueprint