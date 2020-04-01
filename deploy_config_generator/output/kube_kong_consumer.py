import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_kong_consumer'
    DESCR = 'Kubernetes KongConsumer output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kong_consumers': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                username=dict(
                    type='str',
                ),
                custom_id=dict(
                    type='str',
                ),
                credentials=dict(
                    type='list',
                    subtype='str',
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'configuration.konghq.com/v1',
            'kind': 'KongConsumer',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        for field in ('username', 'custom_id', 'credentials'):
            if app_vars['APP'][field]:
                data.update(self.build_generic(app_vars['APP'], {field: self._fields['kong_consumers'][field]}, camel_case=False))

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
