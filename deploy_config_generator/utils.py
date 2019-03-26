from __future__ import print_function

import json
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
    return yaml.safe_dump(value, **kwargs)


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
            if depth is not None:
                tmp_depth = depth - 1
            dict_to[k] = dict_merge(dict_to[k], dict_from[k], depth=tmp_depth)
        else:
            dict_to[k] = dict_from[k]
    return dict_to
