Marking
=======

Marking may be most useful part of `Flask-Swag`. You can add extra fields to operation
object of view function like ``parameters``, ``responses``, etc...

Examples
--------

1. Marking extra fields
~~~~~~~~~~~~~~~~~~~~~~~

You can add arbitrary fields like ::

   @app.route('/some-api')
   @swag.mark({
      'summary': "Summary of API."
   })
   def some_api():
       ...

:class:`~flask_swag.mark.Mark` provides various shortcuts to adding fields.

2. Marking summary
~~~~~~~~~~~~~~~~~~

You can rewrite example above like ::

   @app.route('/some-api')
   @swag.mark.summary("Summary of API.")
   def some_api():
       ...

3. Marking simple parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parameters can be added simply like ::

   @app.route('/some-list')
   @swag.mark.simple_param('query', 'page', int)
   def some_api():
       ...

Or like this ::

   @app.route('/some-list')
   @swag.mark.query('page', int)
   def some_api():
       ...

4. Marking responses
~~~~~~~~~~~~~~~~~~~~

You can add response info like ::

   @app.route('/some-api')
   @swag.mark.response(200, {
       'description': "Returns something.",
       'schema': some_schema,
       'headers': headers,
   })
   def some_api():
       ...

It alose has shorcut ::

   @app.route('/some-api')
   @swag.mark.response(200, "Returns something.", some_schema, headers)
   def some_api():
       ...

For more details, see api references for :class:`flask_swag.mark.Mark`.
