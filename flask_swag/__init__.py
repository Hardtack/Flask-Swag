"""
flask_swag
==========

Flask extension that extracts swagger spec from flask app & provides
Swagger UI.

"""
import os
import urllib.parse

from flask import Flask, Blueprint, current_app, jsonify, \
    send_from_directory, url_for, request

from . import core
from .extractor import Extractor, MarkExtractor
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

    The extension requires following configurations.

            *   SWAG_TITLE

                Title for swagger info.

            *   SWAG_API_VERSION

                API version info.

    Or you can provide `core.Info` instead of them.

    """
    def __init__(self, app: Flask=None, extractor: Extractor=None,
                 *args, **kwargs):
        """
        :param app: app to be initialized
        :param extractor: extractor instance, default is
                          :class:`.extractor.MarkExtractor`
        :param \*args: args to be passed to :meth:`init_app`
        :param \*\*kwargs: kwargs to be passed to :meth:`init_app`

        """
        self.app = app
        self.extractor = extractor or MarkExtractor()
        if app is not None:
            self.init_app(app, *args, **kwargs)

    def init_app(self, app, blueprint_name='swag', prefix='/swagger',
                 swagger_ui_root=SWAGGER_UI_DIR, swagger_info=None,
                 swagger_fields=None):
        """Init flask app for Flask-Swag."""
        def generate_swagger():
            return self.generate_swagger(
                app, swagger_info, swagger_fields, blueprint_name)
        app.generate_swagger = generate_swagger
        self.register_blueprint(app,
                                blueprint_name=blueprint_name,
                                prefix=prefix,
                                swagger_ui_root=swagger_ui_root)

    def generate_swagger(self, app: Flask=current_app, swagger_info=None,
                         swagger_fields=None, swag_blueprint='swag',
                         extractor_kwargs=None):
        """
        Generate swagger spec from `app`.

        :param app: the flask app.

        :param swagger_info: `info` field in swagger root object.

        :param swagger_fields: extra fields in swagger root object.

        :param swag_blueprint: the name of Flask-Swag blueprint

        :extractor_kwargs: kwargs to be passed to extractor's
                           :meth:`extract_paths`

        """
        # Normalize args
        swagger_fields = swagger_fields or {}
        swagger_info = swagger_info or core.Info(
            title=app.config['SWAG_TITLE'],
            version=app.config['SWAG_API_VERSION'],
        )
        # Extract info from current request
        parsed = urllib.parse.urlparse(request.host_url)
        schemes = [parsed.scheme]
        host = parsed.netloc

        # Extract paths from app
        ex_kwargs = {
            'exclude_blueprint': swag_blueprint,
        }
        ex_kwargs.update(extractor_kwargs or {})
        paths = self.extractor.extract_paths(app, **ex_kwargs)

        # Build kwargs for core.Swagger
        kwargs = {
            'info': swagger_info,
            'host': host,
            'schemes': schemes,
            'version': "2.0",
            'paths': paths,
        }

        # Update with swagger_fields
        kwargs.update(swagger_fields)
        return core.convert(core.Swagger(**kwargs))

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
            swagger = current_app.generate_swagger()
            return jsonify(swagger)

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

    def register_blueprint(self, app: Flask, blueprint_name='swag',
                           prefix='/swagger', swagger_ui_root=SWAGGER_UI_DIR) \
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
