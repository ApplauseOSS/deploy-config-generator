from deploy_config_generator.display import Display
from deploy_config_generator.errors import DeployConfigError
from deploy_config_generator.utils import yaml_load


class DeployConfig(object):

    _display = None
    _data = None
    _vars = None
    _path = None
    _version = None

    def __init__(self, path, varset):
        self._vars = varset
        self._display = Display()
        self.load(path)

    def get_config(self):
        return self._data

    def set_config(self, config):
        self._data = config

    def get_version(self):
        return self._version

    def load(self, path):
        self._path = path
        try:
            self._display.v('Loading deploy config file %s' % path)
            with open(path) as f:
                self._data = yaml_load(f.read())
            if not isinstance(self._data, dict):
                raise DeployConfigError('YAML file should contain a top-level dict', path=path)
            if 'version' in self._data:
                self._version = self._data['version']
                del self._data['version']
            for k, v in self._data.items():
                # Wrap the config in a list if it's not already a list
                # This makes it easier to process
                if not isinstance(v, list):
                    self._data[k] = [v]
        except DeployConfigError:
            raise
        except Exception as e:
            raise DeployConfigError('unexpected exception: %s' % str(e))

    def validate_sections(self, valid_sections):
        for section in self._data:
            if section not in valid_sections:
                raise DeployConfigError("section name '%s' is not valid for available plugins" % section)
