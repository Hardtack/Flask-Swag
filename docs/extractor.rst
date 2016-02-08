Extractor
=========

You can extract swagger spec from flask's view function using
:mod:`flask_swag.extractor`. And you can also customize it.

:class:`~flask_swag.extractor.base.Extractor`
---------------------------------------------

This is base class & implementation of extractor.

:meth:`~flask_swag.extractor.base.Extractor.extract_paths` method excutes extraction,
and returns list of path items.


Fields
~~~~~~

Basic implementation of extractor extracts following fields from view functions.


*   description

    Extracts description from docstring & normalizes indentations from.
    :meth:`~flask_swag.extractor.base.Extractor.extract_description`

*   summary

    Extracts summary from first line of description from
    :meth:`~flask_swag.extractor.base.Extractor.extract_summary`.
    It will be truncated if first
    line is longer than 120 chars.

*   parameters

    Extracts parameter info from path. Basically, it converts
    `werkzeug converters <http://werkzeug.pocoo.org/docs/latest/routing/#builtin-converters>`_
    to swagger type from
    :meth:`~flask_swag.extractor.base.Extractor.convert_werkzeug_converter`,
    and fallback to function parameter's annotation using
    :meth:`~flask_swag.extractor.base.Extractor.convert_annotation`.

*   responses

    Since responses is required field, it makes empty default reponse from
    :meth:`~flask_swag.extractor.base.Extractor.extract_responses`.



Filtering
~~~~~~~~~

You can filter endpoints by using ``endpoint`` & ``exclude_endpoint`` parameters, and also can filter blueprints by using ``blueprint`` & ``exclude_blueprint`` parameters.

.. note::

   Since flask can have non-blueprint endpoints like ::

      @app.route('/non-blueprint')
      def non_blueprint():
          pass

   Endpoints with ``None`` blueprint means non-blueprint endpoints.
   So, you can collect non-blueprint only endpoints by
   ``extractor.extract_paths(app, blueprint=None)``

Customization
~~~~~~~~~~~~~

You can customize extractor by subclassing :class:`~flask_swag.extractor.base.Extractor`.

:meth:`~flask_swag.extractor.base.Extractor.extract_others` will be best point to override.

:class:`flask_swag.extractor.mark.MarkExtractor` is simple example for customization.


:class:`~flask_swag.extractor.mark.MarkExtractor`
-------------------------------------------------

Mark extractor extracts extra swagger specs from view functions.
This is the default extractor of :class:`flask_swag.Swag`.

This will be useful when you want to write parameter info to view functions.
