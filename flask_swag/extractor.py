"""
extractor
=========

Extract path info from flask application.

"""
import io

from flask import Flask
from werkzeug.routing import parse_rule

from .core import PathItem, Operation


def convert_werkzeug_rule(rule):
    with io.StringIO() as buf:
        for conv, arg, var in parse_rule(rule):
            if conv:
                buf.write('{')
                buf.write(var)
                buf.write('}')
            else:
                buf.write(var)
        return buf.getvalue()


def normalize_indent(docstring):
    return docstring


def view_to_operation(view):
    description = view.__doc__ or ''
    summary = description.strip().split('\n')[0][:120]

    return Operation(
        description=description,
        summary=summary,
    )


def extract_paths(app: Flask, endpoint=None, from_docstring=True):
    rules = app.url_map.iter_rules(endpoint)

    # Collect endpoints from rules
    endpoints = {}
    for rule in rules:
        path = convert_werkzeug_rule(rule.rule)
        methods = rule.methods.difference({'HEAD', 'OPTIONS'})
        collection = endpoints.setdefault(path, {})
        for method in methods:
            collection[method] = rule.endpoint

    paths = {}
    for path, collection in endpoints.items():
        operations = {}
        for method, endpoint in collection.items():
            view = app.view_functions[endpoint]
            operations[method.lower()] = view_to_operation(view)
        pathitem = PathItem(**operations)
        paths[path] = pathitem
    return paths
