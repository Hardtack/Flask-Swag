"""
fields
======

Definitions of custom fields for marshmallow schema.

"""
from marshmallow import fields


class TypedDict(fields.Field):
    """Typed dict field."""
    def __init__(self, key_field, nested_field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_field = key_field
        self.nested_field = nested_field

    def _add_to_schema(self, field_name, schema):
        super()._add_to_schema(field_name, schema)
        self.key_field._add_to_schema(field_name, schema)
        self.nested_field._add_to_schema(field_name, schema)

    def _deserialize(self, value, attr, data):
        if value is None:
            return None
        ret = {}
        for key, val in value.items():
            k = self.key_field.deserialize(key)
            v = self.nested_field.deserialize(val)
            ret[k] = v
        return ret

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        ret = {}

        def accessor(attr, d, default):
            return d.get(attr, default)

        for key in value:
            k = self.key_field._serialize(key, '', value)
            v = self.nested_field.serialize(key, value, accessor)
            ret[k] = v
        return ret
