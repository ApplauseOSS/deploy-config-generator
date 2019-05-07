import os.path

from six import with_metaclass

from deploy_config_generator.display import Display
from deploy_config_generator.errors import ConfigError
from deploy_config_generator.utils import objdict, yaml_load, Singleton


class SiteConfig(with_metaclass(Singleton, object)):

    _path = None
    _config = None
    _display = None

    _defaults = {
        'default_output': None,
        # Directory within service dir where deploy config is located
        'deploy_dir': 'deploy',
        # Name of deploy config file
        'deploy_config_file': 'config.yml',
        # Directory within deploy dir to look for vars files
        'vars_dir': 'var',
        # Patterns for finding vars files
        'local_vars_file_patterns': ['local.var'],
        'defaults_vars_file_patterns': ['defaults.var'],
        'env_vars_file_patterns': ['{{ env }}.var', 'env_{{ env }}.var'],
        # Whether to use vars from environment
        'use_env_vars': True,
        # Deploy config version to assume if none is provided (defaults to latest)
        'default_config_version': '1',
        # Additional plugins dirs
        'plugin_dirs': [],
        # Plugin-specific options
        'plugins': {},
        # Default apps
        'default_apps': {},
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
            # Handle empty site config file
            # This is mostly here to allow doing '-c /dev/null' in the integration
            # tests to prevent them from picking up the user site config
            if data is None:
                data = {}
            if not isinstance(data, dict):
                raise ConfigError('config file should be formatted as YAML dict')
            self._path = os.path.realpath(path)
            # Special case for plugin dirs
            if 'plugin_dirs' in data:
                if not isinstance(data['plugin_dirs'], list):
                    data['plugin_dirs'] = [data['plugin_dirs']]
                for idx, entry in enumerate(data['plugin_dirs']):
                    if not entry.startswith('/'):
                        # Normalize path based on location of site config
                        data['plugin_dirs'][idx] = os.path.join(os.path.dirname(self._path), entry)
            # Special case for default apps
            if 'default_apps' in data:
                if not isinstance(data['default_apps'], dict):
                    raise ConfigError('"default_apps" key expects a dict, got: %s' % type(data['default_apps']))
                for section, v in data['default_apps'].items():
                    if not isinstance(v, list):
                        raise ConfigError('"default_apps" key expects a dict with section names and a list of default apps')
            self._config.update(data)
        except Exception as e:
            raise ConfigError(str(e))
