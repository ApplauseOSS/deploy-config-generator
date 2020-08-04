import jinja2
import json
import re
import six

from deploy_config_generator.errors import TemplateUndefinedError

OMIT_TOKEN = '__OMIT__TOKEN__'


class Template(object):

    def __init__(self, recursive=True, default_vars=None):
        # Whether to recursively resolve vars
        self._recursive = recursive
        # Default vars
        self._default_vars = default_vars
        # Setup custom Jinja2 Environment instance with our own 'finalize' function,
        # filters, and top-level functions. We use StrictUndefined to raise an exception
        # when accessing an undefined var, so that we can report it to the user
        self._env = jinja2.Environment(finalize=self.finalize, undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        self._env.filters.update(FILTERS)
        self._env.globals.update(GLOBALS)

    @jinja2.contextfunction
    def finalize(self, context, value):
        '''
        This function is called on rendered vars before outputting them. This allows
        us to do recursive templating of vars (vars referencing other vars)
        '''
        # If the value appears to contain a template, render it and return the result
        if self._recursive and isinstance(value, six.string_types):
            if '{{' in value or '{%' in value:
                return context.environment.from_string(value).render(context)

        return value

    def type_fixup(self, value):
        '''
        This function looks for a type header/footer (as added by the various output_*
        Jinja filters) and converts as necessary
        '''
        if isinstance(value, six.string_types):
            # This regex looks for a value like '__int__whatever__int__' and captures
            # the value in the middle
            matches = re.match(r'^__(?P<type>[a-z]+)__(.*)__(?P=type)__$', value)
            if matches:
                value_type = matches.group(1)
                if value_type == 'int':
                    return int(matches.group(2))
                if value_type == 'float':
                    return float(matches.group(2))
                if value_type == 'bool':
                    if matches.group(2).lower() == 'true':
                        return True
                    return False
                if value_type == 'complex':
                    # Parse python complex type from serialized format
                    return eval(matches.group(2))
        return value

    def render_template(self, template, args=None):
        '''
        This function will recursively render templates in strings, dicts, and lists
        '''
        if args is None:
            args = self._default_vars
        if isinstance(template, dict):
            ret = {}
            for k, v in template.items():
                v = self.type_fixup(self.render_template(v, args))
                if v == OMIT_TOKEN:
                    continue
                ret[k] = v
            return ret
        elif isinstance(template, (list, tuple)):
            ret = []
            for i, v in enumerate(template):
                v = self.type_fixup(self.render_template(v, args))
                if v == OMIT_TOKEN:
                    continue
                ret.append(v)
            return ret
        elif isinstance(template, six.string_types):
            try:
                return self._env.from_string(template).render(**args)
            except jinja2.exceptions.UndefinedError as e:
                raise TemplateUndefinedError('undefined value: %s in template: %s' % (str(e), template))
        else:
            return template

    def evaluate_condition(self, condition, tmp_vars):
        '''
        This function uses Jinja to evaluate a conditional statement
        '''
        ret = self._env.from_string('{% if ' + condition + ' %}True{% else %}False{% endif %}').render(**tmp_vars)
        if ret == 'True':
            return True
        return False


def filter_output_int(arg):
    return '__int__' + str(arg) + '__int__'


def filter_output_float(arg):
    return '__float__' + str(arg) + '__float__'


def filter_output_bool(arg):
    return '__bool__' + str(arg) + '__bool__'


def filter_output_complex(arg):
    return '__complex__' + str(arg) + '__complex__'


def filter_to_json(arg, **args):
    return json.dumps(arg, sort_keys=True, **args)


def filter_to_nice_json(arg, indent=2, prefix_indent=None, **args):
    out = filter_to_json(arg, indent=indent, **args)
    # Add extra indentation to all lines to account for being embedded in a
    # larger JSON document
    if prefix_indent:
        out = '\n'.join([ (' ' * prefix_indent) + line for line in out.split('\n') ])
    return out


def filter_default(arg, default):
    '''
    Custom version of default() filter that also returns the default when arg
    is None, in addition to when arg is undefined
    '''
    if arg is None or isinstance(arg, (jinja2.Undefined, jinja2.StrictUndefined)):
        return default
    return arg


def filter_regex_replace(arg, pattern, replacement):
    return re.sub(pattern, replacement, str(arg))


@jinja2.contextfunction
def evaluate_condition(context, condition, **kwargs):
    tmp_vars = context.get_all()
    tmp_vars.update(kwargs)
    ret = context.environment.from_string('{% if ' + condition + ' %}True{% else %}False{% endif %}').render(**tmp_vars)
    if ret == 'True':
        return True
    return False


FILTERS = {
    'output_int': filter_output_int,
    'output_float': filter_output_float,
    'output_bool': filter_output_bool,
    'output_complex': filter_output_complex,
    'to_json': filter_to_json,
    'to_nice_json': filter_to_nice_json,
    'default': filter_default,
    'regex_replace': filter_regex_replace,
}

GLOBALS = {
    'evaluate_condition': evaluate_condition,
    'omit': OMIT_TOKEN,
}
