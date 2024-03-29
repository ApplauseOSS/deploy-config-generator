import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_pv'
    DESCR = 'Kubernetes PersistentVolume output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_pvs': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.PERSISTENT_VOLUME_FIELD_SPEC),
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'v1',
            'kind': 'PersistentVolume',
            'spec': dict(),
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        data['spec'] = self.build_generic(app_vars['APP']['spec'], self._plugin_config['fields']['kube_pvs']['spec']['fields'])

        data = self._template.render_template(data, app_vars)
        output = yaml_dump(data)
        return (output, self.get_output_filename_suffix(data))
