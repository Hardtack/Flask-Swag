"""
mark
====

Mark flask view with swagger spec.

"""
from .utils import merge, normalize_indent


class Mark(object):
    """
    Utility that marks flask view with swagger spec.

    You can add fields to view's operation object using this class. ::

        mark = Mark()

        @app.route('/users/')
        @mark({
            'summary': "List users."
            'produces': ['application/json']
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
        return self.get_swag()

    def merge_swag(self, fn, swag):
        self.set_swag(merge(self.get_swag(fn), swag))

    def swag(self, spec):
        def decorator(fn):
            self.update_swag(fn, spec)
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
