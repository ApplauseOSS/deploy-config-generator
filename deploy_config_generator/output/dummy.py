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
                    'required': True,
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
                    'default': False,
                    'type': 'bool',
                },
            }
        }
    }

    TEMPLATE = '''
    Dummy output plugin

    App config:

    {{ APP | to_nice_json }}
    '''
