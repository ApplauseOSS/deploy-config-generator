from deploy_config_generator.output import OutputPluginBase


class OutputPlugin(OutputPluginBase):

    NAME = 'dummy2'
    DESCR = 'Dummy output plugin for testing'
    FILE_EXT = '.bar'
    PRIORITY = 10

    DEFAULT_CONFIG = {
        'fields': {
            'test2': {
                'dummy2': {
                    'type': 'bool',
                    'description': 'Dummy field',
                    'required': True,
                },
            }
        }
    }

    def generate(self, config):
        for idx, app in enumerate(config['test']):
            config['test'][idx]['var_from_dummy2'] = 'foo'
