import jinja2
import json
import six


# Recursively render template vars
# The concept was adapted from:
# https://stackoverflow.com/a/35320216
def render_template(template, args):
    # The finalize() function is called on rendered vars before outputting them
    def finalize(value):
        # If the value appears to contain a template, render it and return the result
        if isinstance(value, six.string_types) and '{{' in value:
            return env.from_string(value).render(**args)
        return value
    # Setup custom Jinja2 Environment instance with our own 'finalize' function
    env = jinja2.Environment(finalize=finalize)
    env.filters.update(FILTERS)
    return env.from_string(template).render(**args)


def filter_to_json(arg, **args):
    return json.dumps(arg, sort_keys=True, **args)


def filter_to_nice_json(arg, indent=2, prefix_indent=None, **args):
    out = filter_to_json(arg, indent=indent, **args)
    # Add extra indentation to all lines to account for being embedded in a
    # larger JSON document
    if prefix_indent:
        out = '\n'.join([ (' ' * prefix_indent) + line for line in out.split('\n') ])
    return out


FILTERS = {
    'to_json': filter_to_json,
    'to_nice_json': filter_to_nice_json,
}
