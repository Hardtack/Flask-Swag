"""
core
====

Core API for swagger.

"""
import marshmallow

from . import schemas


def make_dict_factory(schema):
    requireds = []
    defaults = {}
    fields = schema.fields

    for name, field in fields.items():
        if field.required:
            requireds.append(name)
        if field.default is not marshmallow.missing:
            defaults[name] = field.default

    def factory(**kwargs):
        strict = kwargs.pop('_strict', True)
        for key, value in defaults.items():
            kwargs.setdefault(key, value)

        for required in requireds:
            if required not in kwargs:
                raise TypeError("Missing argument \"{key}\""
                                .format(key=required))
        if strict:
            for key, value in kwargs.items():
                if key not in fields:
                    raise TypeError("Unexpected argument \"{key}\""
                                    .format(key=key))

        return dict(kwargs)
    return factory


#: Description of external documentation
ExternalDocumentation = make_dict_factory(
    schemas.ExternalDocumentationSchema())

#: Basic schema info
Schema = make_dict_factory(schemas.SchemaSchema())

#: License info
License = make_dict_factory(schemas.LicenseSchema())

#: Contact info
Contact = make_dict_factory(schemas.ContactSchema())

#: Swagger metadata
Info = make_dict_factory(schemas.InfoSchema())

#: Description of items
Items = make_dict_factory(schemas.ItemsSchema())

#: Header info
Header = make_dict_factory(schemas.HeaderSchema())

#: Parameter info
Parameter = make_dict_factory(schemas.ParameterSchema())

#: Description of responses of operation
Response = make_dict_factory(schemas.ResponseSchema())

#: Operations for each method in PathItem
Operation = make_dict_factory(schemas.OperationSchema())

#: Items for each path
PathItem = make_dict_factory(schemas.PathItemSchema())

#: Swagger root object
Swagger = make_dict_factory(schemas.SwaggerSchema())


def dump(swagger, schema=schemas.SwaggerSchema()):
    """
    Dump swagger dict to swagger JSON spec
    """
    return schema.dump(swagger).data


def parameters_from_object_schema(schema, in_='formData'):
    """Convert object schema to parameters."""
    # We can only extract parameters from schema
    if schema['type'] != 'object':
        return []

    properties = schema.get('properties', {})
    required = schema.get('required', [])

    parameters = []
    for name, property in properties.items():
        parameter = {
            'name': name,
            'in_': in_,
            'required': (name in required),
        }
        parameter.update(property)
        parameter = Parameter(**parameter)
        parameters.append(parameter)
    parameters = sorted(parameters, key=lambda x: x['name'])

    return parameters
