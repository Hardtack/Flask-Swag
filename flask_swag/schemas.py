"""
schemas
=======

Definitions of marshmallow schema for swagger specs.

"""
from marshmallow import Schema, fields
from .fields import TypedDict


class MappingSchema(Schema):
    """
    Marshmallow schema whose input is mapping object.
    """
    def get_attribute(self, attr, obj, default):
        return obj.get(attr, default)


class ExternalDocumentationSchema(MappingSchema):
    """
    External documentation object schema

    See http://swagger.io/specification/#externalDocumentationObject

    """
    #: Description
    description = fields.String()

    #: URL
    url = fields.URL(required=True)


class ItemsSchema(MappingSchema):
    """
    Items object schema

    Limited subset of schema object.

    See http://swagger.io/specification/#itemsObject

    """
    #: Type of object
    type = fields.String(required=True)

    #: Format of object type.
    #: See http://swagger.io/specification/#dataTypeFormat
    format = fields.String()

    #: If type is `array`
    items = fields.Nested('self')

    #: How to format collection
    collection_format = fields.String(dump_to='collectionFormat')

    #: Default value
    default = fields.Raw()

    #: Enum of available values
    enum = fields.List(fields.Raw())

    #: Multiple of number
    multiple_of = fields.Number(dump_to='multipleOf')

    #: Maximum
    maximum = fields.Number()

    #: Exclusive maximum
    exclusive_maximum = fields.Number(dump_to='exclusiveMaximum')

    #: Minimum
    minimum = fields.Number()

    #: Exclusive minimum
    exclusive_minimum = fields.Number(dump_to='exclusiveMinimum')

    #: Maximum length
    max_length = fields.Integer(dump_to='maxLength')

    #: Minimum length
    min_length = fields.Integer(dump_to='minLength')

    #: Maximum items
    max_items = fields.Integer(dump_to='maxItems')

    #: Minimum items
    min_items = fields.Integer(dump_to='minItems')

    #: Unique number of items
    unique_items = fields.Integer(dump_to='uniqueItems')

    #: Maximum properties
    max_properties = fields.Integer(dump_to='maxProperties')

    #: Minimum properties
    min_properties = fields.Integer(dump_to='minProperties')


class SchemaSchema(MappingSchema):
    """
    Schema object schema

    See http://swagger.io/specification/#schemaObject

    """
    #: JSON reference
    ref = fields.String(dump_to='$ref')

    #: Type of object
    type = fields.String(required=True)

    #: Format of object type.
    #: See http://swagger.io/specification/#dataTypeFormat
    format = fields.String()

    #: Title
    title = fields.String()

    #: Description
    description = fields.String()

    #: Default value
    default = fields.Raw()

    #: List of name of required field
    required = fields.List(fields.String())

    #: Items
    items = fields.Nested(ItemsSchema)

    #: Validate with all of these schemas
    all_of = fields.Nested('self', many=True, dump_to='allOf')

    #: Properties of schema
    properties = TypedDict(fields.String(),
                           TypedDict(fields.String(), fields.Raw()))

    #: Accepts additional properties?
    additional_properties = fields.Boolean(dump_to='additionalProperties')

    #: Pattern
    pattern = fields.String()

    #: Enum of available values
    enum = fields.List(fields.Raw())

    #: Multiple of number
    multiple_of = fields.Number(dump_to='multipleOf')

    #: Maximum
    maximum = fields.Number()

    #: Exclusive maximum
    exclusive_maximum = fields.Number(dump_to='exclusiveMaximum')

    #: Minimum
    minimum = fields.Number()

    #: Exclusive minimum
    exclusive_minimum = fields.Number(dump_to='exclusiveMinimum')

    #: Maximum length
    max_length = fields.Integer(dump_to='maxLength')

    #: Minimum length
    min_length = fields.Integer(dump_to='minLength')

    #: Maximum items
    max_items = fields.Integer(dump_to='maxItems')

    #: Minimum items
    min_items = fields.Integer(dump_to='minItems')

    #: Unique number of items
    unique_items = fields.Integer(dump_to='uniqueItems')

    #: Maximum properties
    max_properties = fields.Integer(dump_to='maxProperties')

    #: Minimum properties
    min_properties = fields.Integer(dump_to='minProperties')

    #: Add support for polymorphism
    discriminator = fields.String()

    #: Is read-only?
    read_only = fields.Boolean(dump_to='readOnly')

    #: XML metadata
    xml = fields.String()

    #: Additional external document for this schema
    external_docs = fields.Nested(ExternalDocumentationSchema,
                                  dump_to='externalDocs')

    #: Free-form example of schema
    example = fields.Raw()


class LicenseSchema(MappingSchema):
    """
    License object schema

    See http://swagger.io/specification/#licenseObject

    """
    #: Name
    name = fields.String(required=True)

    #: URL
    url = fields.URL()


class ContactSchema(MappingSchema):
    """
    Contact object schema

    See http://swagger.io/specification/#contactObject

    """
    #: Name
    name = fields.String()

    #: URL
    url = fields.URL()

    #: email
    email = fields.Email()


class InfoSchema(MappingSchema):
    """
    Swagger API metadata object schema.

    See http://swagger.io/specification/#infoObject

    """
    #: Title of application
    title = fields.String(required=True)

    #: Short description
    description = fields.String()

    #: Terms of service
    terms_of_service = fields.String(dump_to='termsOfService')

    #: Contact info for API
    contact = fields.Nested(ContactSchema)

    #: License of API
    license = fields.Nested(LicenseSchema)

    #: Version of API, not a version of swagger spec
    version = fields.String(required=True)


class HeaderSchema(MappingSchema):
    """
    Header object schema

    See http://swagger.io/specification/#headerObject

    """
    #: Description of the header
    description = fields.String()

    #: Type of parameter
    type = fields.String(required=True)

    #: Format of parameter
    format = fields.String()

    #: Describe items in array (if type if `array`)
    items = fields.Nested(ItemsSchema)

    #: How to format collection
    collection_format = fields.String(dump_to='collectionFormat')

    #: Pattern
    pattern = fields.String()

    #: Enum of available values
    enum = fields.List(fields.Raw())

    #: Multiple of number
    multiple_of = fields.Number(dump_to='multipleOf')

    #: Maximum
    maximum = fields.Number()

    #: Exclusive maximum
    exclusive_maximum = fields.Number(dump_to='exclusiveMaximum')

    #: Minimum
    minimum = fields.Number()

    #: Exclusive minimum
    exclusive_minimum = fields.Number(dump_to='exclusiveMinimum')

    #: Maximum length
    max_length = fields.Integer(dump_to='maxLength')

    #: Minimum length
    min_length = fields.Integer(dump_to='minLength')

    #: Maximum items
    max_items = fields.Integer(dump_to='maxItems')

    #: Minimum items
    min_items = fields.Integer(dump_to='minItems')

    #: Unique number of items
    unique_items = fields.Integer(dump_to='uniqueItems')

    #: Examples
    examples = TypedDict(fields.String(), fields.Raw())


class ParameterSchema(MappingSchema):
    """
    Parameter object schema

    See http://swagger.io/specification/#parameterObject

    """
    #: Parameter name
    name = fields.String(required=True)

    #: In where?
    in_ = fields.String(dump_to='in')

    #: Brief description
    description = fields.String()

    #: Is required field?
    required = fields.Boolean()

    # If `in` is `body`
    # -------------------------------------------------------------------------

    #: Body's schema
    schema = fields.Nested(SchemaSchema)

    # If `in` is not `body`
    # -------------------------------------------------------------------------

    #: Type of parameter
    type = fields.String()

    #: Format of parameter
    format = fields.String()

    #: Allows empty value?
    allow_empty_value = fields.Boolean(dump_to='allowEmptyValue')

    #: Describe items in array (if type if `array`)
    items = fields.Nested(ItemsSchema)

    #: How to format collection
    collection_format = fields.String(dump_to='collectionFormat')

    #: Pattern
    pattern = fields.String()

    #: Enum of available values
    enum = fields.List(fields.Raw())

    #: Multiple of number
    multiple_of = fields.Number(dump_to='multipleOf')

    #: Maximum
    maximum = fields.Number()

    #: Exclusive maximum
    exclusive_maximum = fields.Number(dump_to='exclusiveMaximum')

    #: Minimum
    minimum = fields.Number()

    #: Exclusive minimum
    exclusive_minimum = fields.Number(dump_to='exclusiveMinimum')

    #: Maximum length
    max_length = fields.Integer(dump_to='maxLength')

    #: Minimum length
    min_length = fields.Integer(dump_to='minLength')

    #: Maximum items
    max_items = fields.Integer(dump_to='maxItems')

    #: Minimum items
    min_items = fields.Integer(dump_to='minItems')

    #: Unique number of items
    unique_items = fields.Integer(dump_to='uniqueItems')


class ResponseSchema(MappingSchema):
    """
    Single response object schema

    See http://swagger.io/specification/#responseObject

    """
    #: Description of response
    description = fields.String(required=True)

    #: Response body's structure
    schema = fields.Nested(SchemaSchema)

    #: Headers of response
    headers = TypedDict(fields.String(), fields.Nested(HeaderSchema))


class OperationSchema(MappingSchema):
    """
    Single API operation on path object schema

    See http://swagger.io/specification/#operationObject

    """
    #: List of tags
    tags = fields.List(fields.String())

    #: Short summary of operation should be less than 120 chars.
    #: But we'll not define max length for capability.
    summary = fields.String()

    #: Long description of operation
    description = fields.String()

    #: Additional external document
    external_docs = fields.Nested(ExternalDocumentationSchema,
                                  dump_to='externalDocs')

    #: Optional unique ID for the operaion
    operation_id = fields.String(dump_to='operationId')

    #: MIME types can be consumed
    consumes = fields.List(fields.String())

    #: MIME types can be produced
    produces = fields.List(fields.String())

    #: Parameters
    parameters = fields.Nested(ParameterSchema, many=True)

    #: Map ofresponses of the operation
    #: The key is status code (int) or 'default'
    responses = TypedDict(fields.Raw(), fields.Nested(ResponseSchema))

    #: Schemes that is supported by this operation
    schemes = fields.List(fields.String())

    #: Is deprecated operation?
    deprecated = fields.Boolean()

    # TODO: Add security field


class PathItemSchema(MappingSchema):
    """
    Path item object schema

    See http://swagger.io/specification/#pathItemObject

    """
    #: GET method for this path item
    get = fields.Nested(OperationSchema)

    #: POST method for this path item
    post = fields.Nested(OperationSchema)

    #: PUT method for this path item
    put = fields.Nested(OperationSchema)

    #: DELETE method for this path item
    delete = fields.Nested(OperationSchema)

    #: OPTIONS method for this path item
    options = fields.Nested(OperationSchema)

    #: HEAD method for this path item
    head = fields.Nested(OperationSchema)

    #: PATCH method for this path item
    patch = fields.Nested(OperationSchema)

    #: Parameters
    parameters = fields.Nested(ParameterSchema, many=True)


class SwaggerSchema(MappingSchema):
    """
    Root swagger document object schema.

    See http://swagger.io/specification/#swaggerObject

    """
    #: Swagger spec version.
    version = fields.String(required=True, dump_to='swagger')

    #: API Metadata
    info = fields.Nested(InfoSchema, required=True)

    #: Host address of API server
    host = fields.String()

    #: Prefix of API URL. Must be started with `/`
    base_path = fields.String(dump_to='basePath')

    #: Schemes of API server
    schemes = fields.List(fields.String())

    #: MIME types can be consumed
    consumes = fields.List(fields.String())

    #: MIME types can be produced
    produces = fields.List(fields.String())

    #: Paths of API
    paths = TypedDict(fields.String(), fields.Nested(PathItemSchema))

    #: Definitions
    definitions = TypedDict(fields.String(), fields.Nested(SchemaSchema))

    #: Predefined parameters that can be reused
    parameters = TypedDict(fields.String(), fields.Nested(ParameterSchema))

    #: Predefined responses that can be reused
    responses = TypedDict(fields.String(), fields.Nested(ResponseSchema))

    #: Additional external document
    external_docs = fields.Nested(ExternalDocumentationSchema,
                                  dump_to='externalDocs')

    # TODO: Add securty, securityDefinitions, tags fields
