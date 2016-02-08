"""
mark
====

Mark flask view with swagger spec.

"""
from marshmallow import Schema as MaSchema

from . import core, ext
from .utils import merge, normalize_indent, compose, get_type_base


class Mark(object):
    """
    Utility that marks flask view with swagger spec.

    You can add fields to view's operation object using this class. ::

        mark = Mark()

        @app.route('/users/')
        @mark({
            'summary': "List users.",
            'produces': ['application/json'],
        })
        def index():
            return jsonify(get_users())

    The mark will be saved to `_swag` property of view function.
    So the `@mark` decorator should be located right under the `@app.route`.

    You can also use convinience methods like :meth:`responses`,
    :meth:`summary`, ... ::

          @app.route('/users/', methods=['POST'])
          @mark.summary("Create a new user")
          def create():
              pass

    You can remove some field from spec by using :meth:`unmark` ::

          @app.route('/users/<int:user_id')
          @mark.unmark('description')
          @mark({
              'summary': "Read a user",
              'description': "Wooah"
          })
          def read(user_id):
              pass

    """
    def __init__(self):
        super().__init__()

    def __call__(self, spec):
        return self.swag(spec)

    def get_swag(self, fn):
        if not hasattr(fn, '_swag'):
            fn._swag = {}
        return fn._swag

    def set_swag(self, fn, swag):
        fn._swag = swag

    def update_swag(self, fn, swag):
        self.get_swag(fn).update(swag)
        return self.get_swag(fn)

    def merge_swag(self, fn, swag):
        self.set_swag(fn, merge(self.get_swag(fn), swag))

    def swag(self, spec):
        def decorator(fn):
            self.update_swag(fn, spec)
            return fn
        return decorator

    def summary(self, summary: str):
        """Mark summary to view."""
        return self.swag({
            'summary': summary
        })

    def description(self, description: str):
        """Mark description to view."""
        return self.swag({
            'description': normalize_indent(description),
        })

    def description_from_docstring(self, fn):
        """Mark description from docstring,"""
        docstring = getattr(fn, '__doc__', None) or ''
        description = normalize_indent(docstring)
        return self.description(description)(fn)

    def summary_from_docstring(self, fn):
        """Mark summary from docstring."""
        docstring = getattr(fn, '__doc__', None) or ''
        description = normalize_indent(docstring)
        summary = description.split('\n', 1)[0].strip()[:120]
        return self.summary(summary)(fn)

    def parameter(self, parameter):
        """Mark parameter to view"""
        def decorator(fn):
            swag = self.get_swag(fn)
            swag.setdefault('parameters', []).append(
                core.Parameter(**parameter))
            self.set_swag(fn, swag)
            return fn
        return decorator

    def schema(self, schema, in_='formData'):
        """Convert json schema to parameter and mark it to view."""
        parameters = core.parameters_from_object_schema(schema, in_=in_)
        return compose(*map(self.parameter, parameters))

    def response(self, status, response_or_description, schema=None,
                 headers=None):
        """Mark response field for view to view.
        There are two ways to use this decorator.

        First, you can pass response object directly ::

            @app.route('/users/<user_id>')
            @mark.response(200, {
                'description': "Target user.",
                'schema': {
                    'properties': {
                        'name': {'type': 'string'},
                    },
                }
            })
            def user_read(user_id):
                ...

        Or you can pass each field of response. ::

            @app.route('/post/<post_id>')
            @mark.response(200, "Target post", post_schema, read_headers)
            def post_read(post_id):
                ...

        `schema` can be marshmallow's :class:`~marshmallow.Schema` if
        `marshmallow_jsonschema` is installed.

        """
        if isinstance(response_or_description, str):
            description = response_or_description
            response = {
                'description': description,
            }
            if schema is not None:
                response['schema'] = schema
            if headers is not None:
                response['headers'] = headers
        else:
            response = response_or_description
        if isinstance(response.get('schema', None), MaSchema):
            response['schema'] = ext.dump_marshmallow(response['schema'])

        def decorator(fn):
            swag = self.get_swag(fn)
            swag.setdefault('responses', {})[status] = core.Response(
                **response)
            self.set_swag(fn, swag)
            return fn
        return decorator

    def simple_param(self, in_, name, python_type, optional=False, **kwargs):
        """
        Mark parameter with python type that can be converted by
        :func:`~.utils.get_type_base`

        """
        required = not optional
        params = (get_type_base(python_type) or {}).copy()
        params.update(
            name=name,
            in_=in_,
            required=required,
        )
        params.update(kwargs)
        return self.parameter(core.Parameter(**params))

    def query(self, name, python_type, optional=False, **kwargs):
        """Mark simple query parameter."""
        return self.simple_param('query', name, python_type, optional=optional,
                                 **kwargs)

    def form(self, name, python_type, optional=False, **kwargs):
        """Mark simple form parameter."""
        return self.simple_param('formData', name, python_type,
                                 optional=optional, **kwargs)

    def formencode(self, formencode_schema, in_='formData'):
        """Mark formencode schema as parameter."""
        return self.schema(ext.dump_formencode(formencode_schema), in_=in_)

    def marshmallow(self, formencode_schema, in_='formData'):
        """Mark marshmallow schema as parameter."""
        return self.schema(ext.dump_marshmallow(formencode_schema), in_=in_)
