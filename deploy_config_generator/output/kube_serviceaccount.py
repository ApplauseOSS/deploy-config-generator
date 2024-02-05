import copy

from deploy_config_generator.utils import yaml_dump, underscore_to_camelcase
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_serviceaccount'
    DESCR = 'Kubernetes service account output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_serviceaccounts': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                automount_service_account_token=dict(
                    type='bool',
                ),
                secrets=dict(
                    type='list',
                    subtype='dict',
                    fields=dict(
                        name=dict(
                            type='str',
                        ),
                    ),
                ),
                image_pull_secrets=dict(
                    type='list',
                    subtype='dict',
                    fields=dict(
                        name=dict(
                            type='str',
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
            'kind': 'ServiceAccount',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        for field in ('automount_service_account_token', 'secrets', 'image_pull_secrets'):
            if app_vars['APP'].get(field, None) is not None and app_vars['APP'][field]:
                data[underscore_to_camelcase(field)] = app_vars['APP'][field]

        data = self._template.render_template(data, app_vars)
        output = yaml_dump(data)
        return (output, self.get_output_filename_suffix(data))
