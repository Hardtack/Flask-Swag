"""
extractor
=========

Extract path info from flask application.

"""
import io
import inspect

from flask import Flask
from werkzeug.routing import parse_rule

from .core import PathItem, Operation, Parameter, Response
from .utils import get_type_base, TYPE_MAP


CONVERTER_TYPES = {
	'float': float,
	'path': str,
	'any': str,
	'default': str,
	'uuid': str,
	'int': int,
	'string': str,
}


def convert_werkzeug_rule(rule):
    params = {}
    with io.StringIO() as buf:
        for conv, arg, var in parse_rule(rule):
            if conv:
                python_type = CONVERTER_TYPES.get(conv, None)
                params[var] = get_type_base(python_type)
                buf.write('{')
                buf.write(var)
                buf.write('}')
            else:
                buf.write(var)
        return buf.getvalue(), params


def normalize_indent(docstring):
    return docstring


def default_response():
    return Response(
        description="Not documented yet.",
    )


def view_to_operation(view, params: dict):
    description = view.__doc__ or ''
    summary = description.strip().split('\n')[0][:120]
    signature = inspect.signature(view)
    responses = {}
    parameters = []
	
    # Extract type info
    for var, converter_type in list(params.items()):
        if converter_type is not None:
            continue
        parameter = signature.parameters.get(var, None)
        if parameter is None:
        	continue
        for available_type in TYPE_MAP:
            if issubclass(parameter.annotation, available_type):
                params[var] = get_type_base(available_type)
                
    for name, type_base in params.items():
        if type_base is None:
            continue
        kwargs = dict(type_base)
        kwargs.update(
            name=name,
            in_='path',
            required=True,
        )
        parameters.append(Parameter(**kwargs))

    # Set default response
    if not responses:
        responses['default'] = default_response()

    return Operation(
        description=description,
        summary=summary,
        parameters=parameters,
        responses=responses,
    )


def get_blueprint_name(endpoint):
    if '.' in endpoint:
        return endpoint.split('.', 1)[0]
    return None


def extract_paths(app: Flask, endpoint=None, blueprint=None, from_docstring=True):
    rules = app.url_map.iter_rules(endpoint)

    # Collect endpoints from rules
    endpoints = {}
    for rule in rules:
        path = rule.rule
        endpoint = rule.endpoint
        if blueprint and blueprint != get_blueprint_name(endpoint):
            continue
        methods = rule.methods.difference({'HEAD', 'OPTIONS'})
        collection = endpoints.setdefault(path, {})
        for method in methods:
            collection[method] = endpoint

    paths = {}
    for rule, collection in endpoints.items():
        path, params = convert_werkzeug_rule(rule)
        operations = {}
        for method, endpoint in collection.items():
            view = app.view_functions[endpoint]
            operations[method.lower()] = view_to_operation(view, params)
        pathitem = PathItem(**operations)
        paths[path] = pathitem
    return paths
