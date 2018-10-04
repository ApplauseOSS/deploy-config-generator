from deploy_config_generator.output import OutputPluginBase


class OutputPlugin(OutputPluginBase):

    NAME = 'dummy'
    DESCR = 'Dummy output plugin for testing'
    FILE_EXT = '.foo'

    FIELDS = [
        {
            'name': 'name',
            'required': True,
        },
        {
            'name': 'image',
            'default': 'applause/{{ SERVICE_NAME }}',
        },
        {
            'name': 'cpus',
            'default': 0.5,
        },
        {
            'name': 'dummy',
            'default': False,
        },
    ]

    TEMPLATE = '''
    Dummy output plugins

    Vars:

    {{ VARS }}

    Config:

    {{ CONFIG }}

    SERVICE_NAME = {{ VARS.SERVICE_NAME | default('N/A') }}
    '''

    def is_needed(self, config):
        if 'dummy' in config:
            return True
        return False
