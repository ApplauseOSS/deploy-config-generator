from six import with_metaclass

from deploy_config_generator.display import Display
from deploy_config_generator.errors import ConfigError
from deploy_config_generator.utils import objdict, yaml_load, Singleton


class SiteConfig(with_metaclass(Singleton, object)):

    _path = None
    _config = None
    _display = None

    _defaults = {
        'default_output': 'marathon',
        'plugins': {},
    }

    def __init__(self):
        self._display = Display()
        self._config = self._defaults

    def __getattr__(self, key):
        '''Allows object-like access to keys in the _config dict'''
        if key in self._config:
            if False and isinstance(self._config[key], dict):
                return objdict(self._config[key])
            return self._config[key]
        else:
            raise AttributeError('No such attribute/key: %s' % key)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setattr__(self, key, value):
        '''Allow setting of internal attributes'''
        if key.startswith('_'):
            super(SiteConfig, self).__setattr__(key, value)
        else:
            raise AttributeError('Config object is not directly writeable')

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __contains__(self, key):
        '''Allows using 'in' keyword'''
        if key in self._config:
            return True
        return False

    def get_config(self):
        return self._config

    def load(self, path):
        try:
            self._display.v('Loading site config from %s' % path)
            with open(path) as f:
                data = yaml_load(f)
            if not isinstance(data, dict):
                raise ConfigError('config file should be formatted as YAML dict')
            self._path = path
            self._config.update(data)
        except Exception as e:
            raise ConfigError(str(e))
