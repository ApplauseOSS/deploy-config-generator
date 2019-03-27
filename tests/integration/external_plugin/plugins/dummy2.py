import inspect

from deploy_config_generator.utils import json_dump
from deploy_config_generator.output import OutputPluginBase


class OutputPlugin(OutputPluginBase):

    NAME = 'dummy2'
    DESCR = 'Dummy output plugin for testing'
    FILE_EXT = '.bar'

    DEFAULT_CONFIG = {
        'fields': {
            'test2': {
                'dummy2': {
                    'default': False,
                    'type': 'bool',
                    'description': 'Dummy field',
                    'required': True,
                },
            }
        }
    }

    TEMPLATE = '''
    Dummy2 output plugin

    App config:
    '''

    def generate_output(self, app_vars):
        output = inspect.cleandoc(self.TEMPLATE)
        output += "\n\n"
        output += json_dump(self._template.render_template(app_vars['APP'], app_vars))
        return output
