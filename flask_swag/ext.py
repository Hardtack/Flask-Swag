"""
ext
===

Utilities for optional external libraries.

"""


def dump_formencode(formencode_schema):
    """Dump formencode schema to json schema using [forencode_jsonschema](
    https://github.com/Hardtack/formencode_jsonschema)

    """
    try:
        import formencode_jsonschema
    except ImportError as e:
        raise ImportError("formencode_jsonschema is required to dump "
                          "formencode schema.") from e
    return formencode_jsonschema.JSONSchema().dump(formencode_schema).data


def dump_marshmallow(marshmallow_schema):
    """
    Dump marshmallow schema to json schema using [marshmallow-jsonschema](
    https://github.com/fuhrysteve/marshmallow-jsonschema)

    """
    try:
        import marshmallow_jsonschema
    except ImportError as e:
        raise ImportError("marshmallow_jsonschema is required to dump "
                          "marshmallow schema.") from e
    return marshmallow_jsonschema.dump(marshmallow_schema)
