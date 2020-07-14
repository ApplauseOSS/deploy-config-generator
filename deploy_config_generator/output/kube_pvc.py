import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_pvc'
    DESCR = 'Kubernetes PersistentVolumeClaim output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_pvcs': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    required=True,
                    fields=dict(
                        access_modes=dict(
                            type='list',
                            subtype='str',
                        ),
                        data_source=dict(
                            type='dict',
                            fields=dict(
                                api_group=dict(
                                    type='str',
                                ),
                                kind=dict(
                                    type='str',
                                ),
                                name=dict(
                                    type='str',
                                ),
                            ),
                        ),
                        resources=dict(
                            type='dict',
                            fields=dict(
                                limits=dict(
                                    type='dict',
                                ),
                                requests=dict(
                                    type='dict',
                                ),
                            ),
                        ),
                        selector=dict(
                            type='dict',
                            fields=copy.deepcopy(kube_common.SELECTOR_FIELD_SPEC),
                        ),
                        storage_class_name=dict(
                            type='str',
                        ),
                        volume_mode=dict(
                            type='str',
                        ),
                        volume_name=dict(
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
            'kind': 'PersistentVolumeClaim',
            'spec': dict(),
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        data['spec'] = self.build_generic(app_vars['APP']['spec'], self._plugin_config['fields']['kube_pvcs']['spec']['fields'])

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
