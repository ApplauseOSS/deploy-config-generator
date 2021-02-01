import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_configmap'
    DESCR = 'Kubernetes ConfigMap output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_configmaps': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                data=dict(
                    type='dict',
                    required=True,
                    subtype='str',
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        data['data'] = app_vars['APP']['data']

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
