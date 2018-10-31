import inspect
import os.path

from deploy_config_generator.site_config import SiteConfig
from deploy_config_generator.display import Display
from deploy_config_generator.template import Template
from deploy_config_generator.errors import DeployConfigGenerationError, ConfigError
from deploy_config_generator.utils import yaml_dump, show_traceback, dict_merge


class OutputPluginBase(object):

    '''
    Base class for output plugins
    '''

    _vars = None
    _output_dir = None
    _display = None
    _section = None

    DEFAULT_CONFIG = {}

    def __init__(self, varset, output_dir):
        self._vars = varset
        self._output_dir = output_dir
        self._display = Display()
        self._display.v('Loading plugin %s' % self.NAME)
        self._template = Template()
        self._site_config = SiteConfig()
        # Build plugin config
        self._plugin_config = self.DEFAULT_CONFIG.copy()
        if self.NAME in self._site_config.plugins:
            for k, v in self._site_config['plugins'][self.NAME].items():
                if k == 'fields':
                    # Merge fields down to a depth of 3 to allow merging of attributes
                    # for each field rather than overwriting of the entire field config
                    self._plugin_config['fields'] = dict_merge(self._plugin_config['fields'], self._site_config['plugins'][self.NAME]['fields'], depth=3)
                else:
                    if k in self._plugin_config:
                        self._plugin_config[k] = v.copy()
                    else:
                        raise ConfigError('unrecognized option: %s' % k)
        self._display.vvv('Plugin config:')
        self._display.vvv()
        self._display.vvv(yaml_dump(self._plugin_config))
        self._display.vvv()

    def set_section(self, section):
        self._section = section

    def has_field(self, field):
        if self._section in self._plugin_config['fields'] and field in self._plugin_config['fields'][self._section]:
            return True
        return False

    def get_required_fields(self):
        ret = []
        if self._section in self._plugin_config['fields']:
            for k, v in self._plugin_config['fields'].items():
                if v.get('required', False) and not v.get('default', None):
                    ret.append(k)
        return ret

    def is_field_locked(self, field):
        if self._section in self._plugin_config['fields'] and field in self._plugin_config['fields'][self._section]:
            if self._plugin_config['fields'][self._section][field].get('locked', False):
                return True
        return False

    def is_needed(self, app):
        # We aren't needed if we have no fields for the current section
        if self._section not in self._plugin_config['fields']:
            return False
        # We are needed if we're the configured default plugin
        if self._site_config.default_output == self.NAME:
            return True
        return True

    def merge_with_field_defaults(self, app):
        ret = {}
        # Apply defaults
        for field, value in self._plugin_config['fields'][self._section].items():
            # If no default is specified, use None. This way, all fields always
            # have a value
            ret[field] = value.get('default', None)
        # Apply values from app config
        ret.update(app)
        return ret

    def generate(self, app, index):
        try:
            path = os.path.join(self._output_dir, '%s-%03d%s' % (self.NAME, index, self.FILE_EXT))
            # Build vars for template
            # changes
            app_vars = {
                'PLUGIN_NAME': self.NAME,
                'APP_INDEX': index,
                'OUTPUT_FILE': os.path.basename(path),
                'OUTPUT_PATH': path,
                # Plugin config
                'CONFIG': self._plugin_config.copy(),
                # App config
                'APP': self.merge_with_field_defaults(app),
                # Parsed vars
                'VARS': dict(self._vars),
            }
            output = self.generate_output(app_vars)
            self._display.v('Writing output file %s' % path)
            with open(path, 'w') as f:
                f.write(output)
        except Exception as e:
            show_traceback(self._display.get_verbosity())
            raise DeployConfigGenerationError(str(e))

    def generate_output(self, app_vars):
        output = self._template.render_template(inspect.cleandoc(self.TEMPLATE), app_vars)
        return output
