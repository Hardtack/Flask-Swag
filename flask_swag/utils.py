import datetime
import decimal
import re
import uuid

# From https://github.com/fuhrysteve/marshmallow-jsonschema/blob/master/marshmallow_jsonschema/base.py
TYPE_MAP = {
    dict: {
        'type': 'object',
    },
    list: {
        'type': 'array',
    },
    datetime.time: {
        'type': 'string',
        'format': 'time',
    },
    datetime.timedelta: {
        # TODO explore using 'range'?
        'type': 'string',
    },
    datetime.datetime: {
        'type': 'string',
        'format': 'date-time',
    },
    datetime.date: {
        'type': 'string',
        'format': 'date',
    },
    uuid.UUID: {
        'type': 'string',
        'format': 'uuid',
    },
    str: {
        'type': 'string',
    },
    bytes: {
        'type': 'string',
    },
    decimal.Decimal: {
        'type': 'number',
        'format': 'decimal',
    },
    set: {
        'type': 'array',
    },
    tuple: {
        'type': 'array',
    },
    float: {
        'type': 'number',
        'format': 'float',
    },
    int: {
        'type': 'integer',
    },
    bool: {
        'type': 'boolean',
    },
}


def get_type_base(python_type) -> dict:
    """Get base schema for python type."""
    return TYPE_MAP.get(python_type, None)


def parse_endpoint(endpoint):
    """
    Parse endpoint into (blueprint, endpoint).
    blueprint can be :const:`None`
    """
    if '.' in endpoint:
        return endpoint.split('.', 1)
    return None, endpoint


def normalize_indent(docstring):
    """
    Normalized indent of docstring.
    """
    lines = docstring.split('\n')
    # Ignore first line
    first = lines.pop(0)
    common_indent = None
    for line in lines:
        if not line.strip():
            # Ignore empty lines
            continue
        indent = re.match(r'^\s*', line).group()
        if common_indent is None:
            common_indent = indent
        # Find common parts
        for i in range(len(common_indent) + 1):
            to = len(common_indent) - i
            if indent.startswith(common_indent[:to]):
                common_indent = common_indent[:to]
                break
    normalized = []
    for line in lines:
        line = line[len(common_indent):]
        normalized.append(line)
    normalized.insert(0, first)
    return '\n'.join(normalized)


def merge(dest, src):
    """Merge plain objects without mutation."""
    if isinstance(dest, dict) and isinstance(src, dict):
        dest = dest.copy()
        src = src.copy()
        dest_keys = list(dest.keys())
        for key in dest_keys:
            if key in src:
                dest[key] = merge(dest[key], src.pop(key))
        dest.update(src)
        return dest
    if isinstance(dest, list) and isinstance(src, list):
        dest = dest.copy()
        src = src.copy()
        if len(dest) > len(src):
            tail = dest[len(src):]
        else:
            tail = src[len(dest):]
        merged = []
        for dest_item, src_item in zip(dest, src):
            merged.append(merge(dest_item, src_item))
        merged.extend(tail)
        return merged
    return src


def compose(last, *fn):
    """Compose functions."""
    fn = (last,) + fn

    def composed(*args):
        for f in reversed(fn):
            args = (f(*args), )
        return args[0]
    return composed
