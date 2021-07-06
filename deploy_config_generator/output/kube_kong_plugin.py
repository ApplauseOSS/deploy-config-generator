import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_kong_plugin'
    DESCR = 'Kubernetes KongPlugin output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kong_plugins': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                disabled=dict(
                    type='bool',
                ),
                config=dict(
                    type='dict',
                ),
                config_from=dict(
                    type='dict',
                    fields=dict(
                        secret_key_ref=dict(
                            type='dict',
                            required=True,
                            fields=dict(
                                name=dict(
                                    type='str',
                                    required=True,
                                ),
                                key=dict(
                                    type='str',
                                    required=True,
                                ),
                            ),
                        ),
                    ),
                ),
                plugin=dict(
                    type='str',
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'configuration.konghq.com/v1',
            'kind': 'KongPlugin',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        for field in ('disabled', 'config', 'config_from', 'plugin'):
            if app_vars['APP'][field]:
                data.update(self.build_generic(app_vars['APP'], {field: self._fields['kong_plugins'][field]}))

        data = self._template.render_template(data, app_vars)
        output = yaml_dump(data)
        return (output, self.get_output_filename_suffix(data))
