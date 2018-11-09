from deploy_config_generator.display import Display
from deploy_config_generator.errors import DeployConfigError, VarsReplacementError
from deploy_config_generator.utils import yaml_load

# TODO: build this dynamically from output plugins
VALID_SECTIONS = ('apps', 'jobs', 'test')


class DeployConfig(object):

    _display = None
    _data = None
    _vars = None
    _path = None

    def __init__(self, path, varset):
        self._vars = varset
        self._display = Display()
        self.load(path)

    def get_config(self):
        return self._data

    def load(self, path):
        self._path = path
        try:
            self._display.v('Loading deploy config file %s' % path)
            yaml_content = ''
            with open(path) as f:
                for line_idx, line in enumerate(f):
                    try:
                        yaml_content += self._vars.replace_vars(line)
                    except VarsReplacementError as e:
                        raise DeployConfigError('variable replacement error: %s' % str(e), path=path, line=line_idx + 1)
            self._data = yaml_load(yaml_content)
            if not isinstance(self._data, dict):
                raise DeployConfigError('YAML file should contain a top-level dict', path=path)
            for k, v in self._data.items():
                if k not in VALID_SECTIONS:
                    raise DeployConfigError("section name '%s' is not recognized" % k)
                # Wrap the config in a list if it's not already a list
                # This makes it easier to process
                if not isinstance(v, list):
                    self._data[k] = [v]
        except DeployConfigError:
            raise
        except Exception as e:
            raise DeployConfigError('unexpected exception: %s' % str(e))
