import pytest

from flask_swag.core import parameters_from_object_schema, convert, Swagger, \
    Info, PathItem, Operation, Response, Schema, License


def test_factory():
    # License has required field `name`
    with pytest.raises(TypeError):
        License()
    # Will not raise `TypeError` at here
    License(name='MIT')


def test_dump_swagger():
    swagger = Swagger(
        version='2.0',
        info=Info(
            title='Test REST API',
            version='0.1.0'
        ),
        host='localhost',
        base_path='/api',
        schemes=[],
        paths={
            '/foos/': PathItem(
                get=Operation(
                    summary='Get a list of foos',
                    responses={
                        'default': Response(
                            description='List of foos',
                            schema=Schema(
                                type='object',
                                properties={
                                    'id': {
                                        'type': 'integer',
                                    },
                                },
                            ),
                        ),
                    },
                ),
            ),
        },
    )

    assert {
        'swagger': '2.0',
        'info': {
            'title': 'Test REST API',
            'version': '0.1.0',
        },
        'host': 'localhost',
        'basePath': '/api',
        'schemes': [],
        'paths': {
            '/foos/': {
                'get': {
                    'summary': 'Get a list of foos',
                    'responses': {
                        'default': {
                            'description': 'List of foos',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'id': {
                                        'type': 'integer'
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    } == convert(swagger)


def test_parameters_from_schema():
    json_schema = Schema(**{
        'properties': {
            'description': {'type': 'string'},
            'location': {'type': 'string'},
            'title': {'type': 'string'},
        },
        'required': ['title'],
        'type': 'object',
    })
    parameters = parameters_from_object_schema(json_schema)

    swagger = Swagger(
        version='2.0',
        info=Info(
            title='Test REST API',
            version='0.1.0',
        ),
        paths={
            '/appointments/': PathItem(
                post=Operation(
                    summary='Create an appointment',
                    parameters=parameters,
                    responses={
                        201: Response(
                            description='Created appointment'
                        ),
                    },
                ),
            ),
        },
    )

    assert {
        'swagger': '2.0',
        'info': {
            'title': 'Test REST API',
            'version': '0.1.0',
        },
        'paths': {
            '/appointments/': {
                'post': {
                    'summary': 'Create an appointment',
                    'parameters': [{
                        'name': 'description',
                        'in': 'formData',
                        'type': 'string',
                        'required': False,
                    }, {
                        'name': 'location',
                        'in': 'formData',
                        'type': 'string',
                        'required': False,
                    }, {
                        'name': 'title',
                        'in': 'formData',
                        'type': 'string',
                        'required': True,
                    }],
                    'responses': {
                        201: {
                            'description': 'Created appointment',
                        },
                    },
                },
            },
        },
    } == convert(swagger)


def test_strict():
    # Strict on
    with pytest.raises(TypeError):
        License(
            name='MIT',
            foo='bar',
        )
    # Strict off
    License(
        name='MIT',
        foo='bar',
        _strict=False
    )
