import inspect

from deploy_config_generator.utils import json_dump
from deploy_config_generator.output import OutputPluginBase


class OutputPlugin(OutputPluginBase):

    NAME = 'dummy'
    DESCR = 'Dummy output plugin for testing'
    FILE_EXT = '.foo'

    DEFAULT_CONFIG = {
        'enabled': False,
        'fields': {
            'test': {
                'parent1': {
                    'description': 'Used for tests',
                    'required': False,
                    'type': 'list',
                    'subtype': 'dict',
                    'fields': {
                        'child2_1': {},
                        'child2_2': {},
                        'parent2': {
                            'type': 'list',
                            'subtype': 'dict',
                            'fields': {
                                'child3_1': {},
                                'child3_2': {}
                            }
                        }
                    },
                },
                'dummy': {
                    'type': 'bool',
                    'description': 'Dummy field',
                    'required': True,
                },
            }
        }
    }

    TEMPLATE = '''
    Dummy output plugin

    App config:
    '''

    def generate_output(self, app_vars):
        output = inspect.cleandoc(self.TEMPLATE)
        output += "\n\n"
        output += json_dump(self._template.render_template(app_vars['APP'], app_vars))
        return output
