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

_MISSING = object()

CONVERTER_TYPES = {
	'float': float,
	'path': str,
	'any': str,
	'default': str,
	'uuid': str,
	'int': int,
	'string': str,
}

def parse_endpoint(endpoint):
    """
    Parse endpoint into (blueprint, endpoint).
    blueprint can be :const:`None`
    """
    if '.' in endpoint:
        return endpoint.split('.', 1)
    return None, endpoint


def normalize_indent(docstring):
    return docstring


WerkzeugConverter = collections.namedtuple('WerkzeugConverter', ['converter', 'args', 'kwargs'])
PathAndParams = collections.namedtuple('PathAndParams', ['path', 'params'])
PathAndPathItem = collections.namedtuple('PathAndPathItem', ['path', 'item'])


class Extractor(object):
    """
    Base class that extract swagger spec from flask application.

    You can extract path items from app by using :meth:`extract_paths`
    and customize converting method by overriding them.

    """
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
    
    def extract_responses(self, view):
        return {
            'default': Response(
                description=''
            ),
        }

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

    def extract_others(self, view, params: dict, endpoint: str,
                       path: str, method: str, app: Flask):
        return {}

    def make_operation(self, view, params: dict, endpoint: str,
                       path: str, method: str, app: Flask):
        """Convert view to swagger opration object."""
        description = self.extract_description(view)
        summary = self.extract_summary(view)
        parameters = self.build_parameters(view, params)
        responses = self.extract_responses(view)
        kwargs = self.extract_others(
            view, params, endpoint, path, method, app)

        return Operation(
            description=description,
            summary=summary,
            parameters=parameters,
            responses=responses,
            **kwargs
        )

    def collect_endpoints(self, app: Flask, blueprint=_MISSING, endpoint=None) -> dict:
        """Collect endpoints in rules.

        :param blueprint: name of blueprints to be collected. :const:`None` means
                          non-blueprint endpoints. It cat either be list or string.
        :param endpoint: endpoints to be collected. It cat either be list or string.

        """
        if blueprint is not _MISSING:
            if blueprint is None or isinstance(blueprint, str):
            	blueprint = (blueprint,)
        if isinstance(endpoint, str):
            endpoint = (endpoint,)

        endpoints = {}
        for rule in app.url_map.iter_rules():
            if blueprint is not _MISSING:
                rule_blueprint, rule_endpoint = parse_endpoint(rule.endpoint)
                if rule_blueprint not in blueprint:
                    continue
                if endpoint and rule_endpoint not in endpoint:
                    continue
            elif endpoint and rule.endpoint not in endpoint:
                continue
            methods = rule.methods.difference({'HEAD', 'OPTIONS'})
            method_collection = endpoints.setdefault(rule.rule, {})
            for method in methods:
                method_collection[method] = rule.endpoint
        return endpoints

    def make_path_item(self, app: Flask, rule: str, endpoints: dict) -> PathAndPathItem:
        """Make path item from rule and endpoints collected by HTTP methods."""
        path, params = self.parse_werkzeug_rule(rule)
        operations = {}
        for method, endpoint in endpoints.items():
            view = app.view_functions[endpoint]
            operations[method.lower()] = self.make_operation(
                view, params, endpoint, path, method, app)
        return PathAndPathItem(
            path=path,
            item=PathItem(**operations),
        )


    def extract_paths(self, app: Flask, blueprint=_MISSING, endpoint=None):
        """Extract path items from flask app.

        :param blueprint: name of blueprints to be collected. :const:`None` means
                          non-blueprint endpoints. It cat either be list or string.
        :param endpoint: endpoints to be collected. It cat either be list or string.
        """

        endpoints = self.collect_endpoints(app, blueprint, endpoint)

        paths = {}
        for rule, methods in endpoints.items():
            path, path_item = self.make_path_item(app, rule, methods)
            paths[path] = path_item
        return paths
