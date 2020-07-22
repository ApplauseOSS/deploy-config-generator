from __future__ import print_function

import json
import re
import traceback
import yaml


class objdict(dict):

    '''
    Dict-like object that also allows accessing keys as attributes
    '''

    def __init__(self, d=None):
        self.clear()
        if d:
            self.update(d)

    def __getattr__(self, key):
        if key in self:
            ret = self[key]
            if isinstance(ret, dict):
                # Replace any dicts with objdict objects
                for k, v in ret.items():
                    if isinstance(v, dict):
                        ret[k] = objdict(v)
            return ret
        else:
            raise AttributeError('No such attribute/key: %s' % key)

    def __getitem__(self, key):
        parent = super(objdict, self)
        if parent.__contains__(key):
            ret = parent.__getitem__(key)
            if isinstance(ret, dict):
                # Replace any dicts with objdict objects
                for k, v in ret.items():
                    if isinstance(v, dict):
                        ret[k] = objdict(v)
            return ret
        else:
            raise AttributeError('No such attribute/key: %s' % key)

    def __setattr__(self, key, value):
        self[key] = value

    def to_dict(self):
        ret = {}
        for k, v in self.items():
            if isinstance(v, objdict):
                ret[k] = v.to_dict()
            else:
                ret[k] = v
        return ret


class Singleton(type):

    '''
    Meta-class for singleton objects
    '''

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def show_traceback(verbosity=0):
    '''
    Helper function to display a traceback for the current exception
    '''
    # We can't use Display here without creating a circular dependency
    if verbosity >= 3:
        print('Caught exception:')
        print()
        print(traceback.format_exc())
        print()


def yaml_dump(value, **kwargs):
    return yaml.safe_dump(value, default_flow_style=False, **kwargs)


def yaml_load(value, **kwargs):
    return yaml.safe_load(value, **kwargs)


def json_dump(value, sort_keys=True, indent=2, separators=(',', ': '), **kwargs):
    return json.dumps(value, sort_keys=sort_keys, indent=indent, separators=separators, **kwargs)


def dict_merge(dict_to, dict_from, depth=None):
    '''
    Recursively merge dicts, optionally to a specific depth
    '''
    if depth is not None and depth <= 0:
        return dict_to
    dict_to = dict_to.copy()
    for k in dict_from:
        if k in dict_to and isinstance(dict_to[k], dict) and isinstance(dict_from[k], dict):
            # Continue merging if source and dest are a dict
            if depth is not None:
                depth = depth - 1
            dict_to[k] = dict_merge(dict_to[k], dict_from[k], depth=depth)
        else:
            # Overwrite value
            dict_to[k] = dict_from[k]
    return dict_to


def underscore_to_camelcase(value):
    '''
    Convert field name with underscores to camel case

    This converts 'foo_bar_baz' (the standard for this app) to
    'fooBarBaz' (the standard for Marathon and Kubernetes)
    '''
    def replacer(match):
        # Grab the last character of the match and upper-case it
        return match.group(0)[-1].upper()
    return re.sub(r'_[a-zA-Z]', replacer, value)


# Override boolean definition for YAML dumper to properly quote Y/N values
# This is needed because PyYAML doesn't consider Y/N as boolean values (which
# deviates from the YAML spec), so it doesn't quote them when dumping, but
# kubectl does consider them boolean values, so it misinterprets YAML generated
# by this tool with those string values as being boolean values
yaml.resolver.Resolver.add_implicit_resolver(
    u'tag:yaml.org,2002:bool',
    re.compile(r'^(?:y|Y|n|N|yes|Yes|YES|no|No|NO|true|True|TRUE|false|False|FALSE|on|On|ON|off|Off|OFF)$', re.X),
    list(u'yYnNtTfFoO')
)
