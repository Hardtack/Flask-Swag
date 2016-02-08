"""
flask_swag
==========

Flask extension that extracts swagger spec from flask app & provides
Swagger UI.

"""
import os
import urllib.parse

from flask import Flask, Blueprint, current_app, jsonify, \
    send_from_directory, url_for, request, redirect

from . import core
from .extractor import Extractor, MarkExtractor
from .globals import SWAGGER_UI_DIR
from .mark import Mark
from .version import VERSION


__version__ = VERSION


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

    To customize URL for swagger, use following configurations.

        *   SWAG_BLUEPRINT_NAME

            Default is ``'swag'``

        *   SWAG_URL_PREFIX

            Default is ``'/swagger'``

        *   SWAG_JSON_URL

            Default is ``'/swagger.json'``

        *   SWAG_UI_PREFIX

            Default is ``'/ui'``

    And you can use another version of swagger-ui using configuration.

        *   SWAG_UI_ROOT


    """
    def __init__(self, app: Flask=None, extractor: Extractor=None,
                 mark: Mark=None, *args, **kwargs):
        """
        :param app: app to be initialized
        :param extractor: extractor instance, default is
                          :class:`.extractor.MarkExtractor`
        :param extractor: marker instance, default is
                          :class:`.mark.Mark`
        :param \*args: args to be passed to :meth:`init_app`
        :param \*\*kwargs: kwargs to be passed to :meth:`init_app`

        """
        self.app = app
        self.extractor = extractor or MarkExtractor()
        self.mark = mark or Mark()
        if app is not None:
            self.init_app(app, *args, **kwargs)

    def init_app(self, app, swagger_info=None, swagger_fields=None):
        """Init flask app for Flask-Swag."""
        # Default values for configurations
        app.config.setdefault('SWAG_UI_ROOT', SWAGGER_UI_DIR)
        app.config.setdefault('SWAG_BLUEPRINT_NAME', 'swag')
        app.config.setdefault('SWAG_URL_PREFIX', '/swagger')
        app.config.setdefault('SWAG_JSON_URL', '/swagger.json')
        app.config.setdefault('SWAG_UI_PREFIX', '/ui')

        # Add generator too app
        def generate_swagger():
            return self.generate_swagger(app, swagger_info, swagger_fields)
        app.generate_swagger = generate_swagger

        self.register_blueprint(app)

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
        return core.dump(core.Swagger(**kwargs))

    def inject_swagger_url(self, html, url):
        """
        Change default swagger URL by injecting javascript code into html.
        """
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
        components = html.rsplit('</body>', 1)
        if len(components) == 1:
            html, = components
            components = html.rsplit('</html>', 1)
            if len(components) == 1:
                html = html + tag
            else:
                first, rest = components
                html = first + tag + '</html>' + rest
        else:
            first, rest = components
            html = first + tag + '</body>' + rest
        return html

    def make_blueprint(self, blueprint_name, swagger_ui_root, json_url,
                       ui_prefix) -> Blueprint:
        """
        Create a new Swagger UI related blueprint.

        :param blueprint_name: name of the blueprint. default is `'swag'`
        :param swagger_ui_root: root path for swagger-ui.
        :param json_url: swagger spec json URL.
        :param ui_prefix: prefix URL for swagger-ui

        """
        blueprint = Blueprint(blueprint_name, __name__)

        @blueprint.route(json_url)
        def swagger_json():
            swagger = current_app.generate_swagger()
            return jsonify(swagger)

        @blueprint.route('{}/<path:path>'.format(ui_prefix))
        def swagger_ui(path):
            return send_from_directory(swagger_ui_root, path,
                                       cache_timeout=3600)

        @blueprint.route('{}/'.format(ui_prefix))
        def swagger_ui_index():
            with open(os.path.join(swagger_ui_root, 'index.html')) as f:
                html = f.read()
            # Inject javascript code
            url = url_for('{}.swagger_json'.format(blueprint_name))
            html = self.inject_swagger_url(html, url)
            return html, 200

        @blueprint.route(ui_prefix)
        def swagger_ui_prefix():
            return redirect('{}.swagger_ui_index'.format(blueprint_name))

        return blueprint

    def register_blueprint(self, app: Flask) \
            -> Blueprint:
        """
        Register Swagger UI related blueprint.

        :param blueprint_name: name of the blueprint. default is `'swag'`
        :param prefix: URL prefix of the blueprint.
        :returns: created blueprint

        """
        prefix = app.config['SWAG_URL_PREFIX']
        blueprint_name = app.config['SWAG_BLUEPRINT_NAME']
        swagger_ui_root = app.config['SWAG_UI_ROOT']
        json_url = app.config['SWAG_JSON_URL']
        ui_prefix = app.config['SWAG_UI_PREFIX']

        blueprint = self.make_blueprint(blueprint_name, swagger_ui_root,
                                        json_url, ui_prefix)
        app.register_blueprint(blueprint, url_prefix=prefix)

        return blueprint
