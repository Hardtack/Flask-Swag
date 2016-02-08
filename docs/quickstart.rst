Quick Start
===========

This page is best point to getting started.

You can find out source code from https://github.com/hardtack/flask-swag


Configuring
-----------

There are two ways to configure your app for Flask-Swag, just like other
flask extensions.

First, you can configure on init ::

    from flask.ext.swag import Swag

    swag = Swag(app)


Or you can configure later ::

    from .exts import swag

    swag.init_app(app)


Swagger-UI
----------

By default, you may find out Swagger-UI on ``/swagger/ui/`` provided by blueprint.

.. image:: images/screenshot.png

You can customize Swagger-UI by configuring ``'SWAG_UI_ROOT'``


Marking
-------

You can add additional field to
`operations <http://swagger.io/specification/#operationObject>`_ by marking.

.. code-block:: python

    @app.route('/users/')
    @swag.mark.summary("Get list of users.")
    @swag.mark.query('page', int)
    @swag.mark.response(200, "List of users.", user_list_schema)
    def user_index():
        """
        Get list of users.

        The result will be paginated, default page is 1.
        """
        ...

or for complex operations, you can set operation's fields directly

.. code-block:: python

    @app.route('/users/<int:user_id>')
    @swag.mark({
        'description': "Read user's info.",
        'responses': {
            200: {
                'description': "User object."
                'schema': {
                    'properties': {
                        'name': {'type': 'string'}
                    }
                }
            }
        }
    })
    def user_read(user_id):
        ...

You can mark parameters from formencode.

.. code-block:: python


    from .formencode_schemas import UserCreateSchema


    @app.route('/users/', methods=['POST'])
    @swag.formencode(UserCreateSchema())
    def user_create():
        ...

And you can set resposne's schema from marshmallow.

.. code-block:: python

    from .marshmallow_schemas import UserSchema

    @app.route('/users/<int:user_id')
    @swag.response(200, "User's info", UserSchema())
    def user_read(user_id):
        ...
