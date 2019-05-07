from deploy_config_generator.display import Display
from deploy_config_generator.errors import DeployConfigError
from deploy_config_generator.utils import yaml_load
from deploy_config_generator.template import Template


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

    def apply_default_apps(self, default_apps):
        # These annoying names are to prevent conflicts with fields in the default app definitions
        PLACEMENT_KEY = 'default_placement'
        CONDITION_KEY = 'default_condition'
        for section in default_apps:
            if section not in self._data:
                self._data[section] = []
            insert_idx = 0
            for app in default_apps[section]:
                placement = app.get(PLACEMENT_KEY, 'before')
                if PLACEMENT_KEY in app:
                    del app[PLACEMENT_KEY]
                if CONDITION_KEY in app:
                    condition = app[CONDITION_KEY]
                    del app[CONDITION_KEY]
                    template = Template()
                    tmp_vars = dict(VARS=dict(self._vars))
                    # Continue to next item if we have a condition and it evaluated to False
                    if not template.evaluate_condition(condition, tmp_vars):
                        continue
                if placement in ('before', 'pre'):
                    self._data[section].insert(insert_idx, app)
                    insert_idx += 1
                elif placement in ('after', 'post'):
                    self._data[section].append(app)
                else:
                    raise DeployConfigError('invalid default app placement: %s' % placement)
