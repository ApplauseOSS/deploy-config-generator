import inspect
import os.path

from deploy_config_generator.template import render_template
from deploy_config_generator.errors import ConfigGenerationError


class OutputPluginBase(object):

    '''
    Base class for output plugins
    '''

    _vars = None
    _output_dir = None
    _display = None

    FIELDS = []

    def __init__(self, varset, output_dir, display):
        self._vars = varset
        self._output_dir = output_dir
        self._display = display

    def has_field(self, field):
        for f in self.FIELDS:
            if f['name'].lower() == field.lower():
                return True
        return False

    def is_needed(self, config):
        return False

    def merge_with_field_defaults(self, config):
        ret = {}
        for field in self.FIELDS:
            if 'default' in field:
                ret[field['name']] = field['default']
        ret.update(config)
        return ret

    def generate(self, config, index):
        try:
            path = os.path.join(self._output_dir, '%s-%03d%s' % (self.NAME, index, self.FILE_EXT))
            # Build vars for template
            # We start with an empty dict and use .update() to prevent issues
            # with getting a ref to any of the source dicts directly and risking
            # changes
            tmp_vars = {}
            tmp_vars.update({
                'PLUGIN_NAME': self.NAME,
                'APP_INDEX': index,
                'OUTPUT_FILE': os.path.basename(path),
                'OUTPUT_PATH': path,
                # App config
                'CONFIG': self.merge_with_field_defaults(config),
                # Parsed vars
                'VARS': dict(self._vars),
            })
            output = render_template(inspect.cleandoc(self.TEMPLATE), tmp_vars)
            self._display.v('Writing output file %s' % path)
            with open(path, 'w') as f:
                f.write(output)
        except Exception as e:
            raise ConfigGenerationError(str(e))
