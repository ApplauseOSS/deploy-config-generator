import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_pdb'
    DESCR = 'Kubernetes PDB output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_pdbs': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    required=True,
                    fields=dict(
                        max_unavailable=dict(
                            type='int',
                        ),
                        min_available=dict(
                            type='int',
                        ),
                        selector=dict(
                            type='dict',
                            fields=dict(
                                match_labels=dict(
                                    type='dict',
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'policy/v1beta1',
            'kind': 'PodDisruptionBudget',
            'spec': dict(),
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        data['spec'] = self.build_generic(app_vars['APP']['spec'], self._plugin_config['fields']['kube_pdbs']['spec']['fields'])

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
