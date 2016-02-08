"""
extractor
=========

Extract path info from flask application.

"""
import io
import inspect
import collections

from flask import Flask
from werkzeug.routing import parse_rule, parse_converter_args

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

def get_blueprint_name(endpoint):
    if '.' in endpoint:
        return endpoint.split('.', 1)[0]
    return None


def normalize_indent(docstring):
    return docstring


WerkzeugConverter = collections.namedtuple('WerkzeugConverter', ['converter', 'args', 'kwargs'])
PathAndParams = collections.namedtuple('PathAndParams', ['path', 'params'])


class Extractor(object):

    def convert_werkzeug_converter(self, name: str, converter: WerkzeugConverter):
        """Convert werkzeug converter to swagger parameter object."""
        python_type = CONVERTER_TYPES.get(converter.converter, None)
        type_base = get_type_base(python_type)
        if type_base is None:
            return None
        return Parameter(name=name, in_="path", required=True, **type_base)

    def convert_annotation(self, name, annotation):
        """Convert function annotation to swagger parameter object."""
        if annotation is None:
            return None
        if not isinstance(annotation, type):
            return None
        type_base = None
        for available_type in TYPE_MAP:
            if issubclass(annotation, available_type):
                type_base = get_type_base(available_type)
                break
        if type_base is None:
        	return None
        return Parameter(name=name, in_="path", **type_base)

    def parse_werkzeug_rule(self, rule: str) -> PathAndParams:
        """
        Convert werkzeug rule to swagger path format and
        extract parameter info.
        """
        params = {}
        with io.StringIO() as buf:
            for converter, arguments, variable in parse_rule(rule):
                if converter:
                    if arguments is not None:
                        args, kwargs = parse_converter_args(arguments)
                    else:
                        args = ()
                        kwargs = {}
                    params[variable] = WerkzeugConverter(
                        converter=converter,
                        args=args,
                        kwargs=kwargs,
                    )
                    buf.write('{')
                    buf.write(variable)
                    buf.write('}')
                else:
                    buf.write(variable)
            return PathAndParams(buf.getvalue(), params)


    def default_response(self):
        return Response(
            description="Not documented yet.",
        )

    def extract_description(self, view) -> str:
        """Extract description info from view function."""
        doc = getattr(view, '__doc__', None) or None
        if not doc:
            return None
        return normalize_indent(doc)

    def extract_summary(self, view) -> str:
        """Extract brief description from view function."""
        description = self.extract_description(view)
        if not description:
            return None
        return description.strip().split('\n', 1)[0][:120].strip()

    def extract_param(self, view, name):
        """Extract path parameters info from view function."""
        signature = inspect.signature(view)
        if name not in signature.parameters:
            return None
        parameter = signature.parameters.get(name)
        annotation = parameter.annotation
        return self.convert_annotation(name, annotation)

    def build_parameters(self, view, param_info) -> list:
        """
        Build parameters from path params and view params.
        path params have higher order.
        """
        parameters = []
        for name, converter in param_info.items():
            parameter = self.convert_werkzeug_converter(name, converter)
            if parameter is None:
                parameter = self.extract_param(view, name)
            if parameter is None:
                continue
            parameters.append(parameter)
        return parameters

    def view_to_operation(self, view, params: dict):
        """Convert view to swagger opration object."""
        description = self.extract_description(view)
        summary = self.extract_summary(view)
        responses = {}
        parameters = self.build_parameters(view, params)

        # Set default response
        if not responses:
            responses['default'] = self.default_response()

        return Operation(
            description=description,
            summary=summary,
            parameters=parameters,
            responses=responses,
        )

    def extract_paths(self, app: Flask, endpoint=None, blueprint=None, from_docstring=True):
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
            path, params = self.parse_werkzeug_rule(rule)
            operations = {}
            for method, endpoint in collection.items():
                view = app.view_functions[endpoint]
                operations[method.lower()] = self.view_to_operation(view, params)
            pathitem = PathItem(**operations)
            paths[path] = pathitem
        return paths
