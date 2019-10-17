import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_namespace'
    DESCR = 'Kubernetes namespace output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_namespaces': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    fields=dict(
                        finalizers=dict(
                            type='list',
                            subtype='str',
                        ),
                    ),
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'v1',
            'kind': 'Namespace',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        if app_vars['APP']['spec']:
            tmp_spec = self.build_generic(app_vars['APP']['spec'], self._plugin_config['fields']['kube_namespaces']['spec']['fields'])
            if tmp_spec:
                data['spec'] = tmp_spec

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
