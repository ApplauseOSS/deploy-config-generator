import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_service'
    DESCR = 'Kubernetes service output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_services': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    required=True,
                    fields=dict(
                        cluster_IP=dict(
                            type='str',
                        ),
                        external_IPs=dict(
                            type='list',
                            subtype='str',
                        ),
                        external_name=dict(
                            type='str',
                        ),
                        external_traffic_policy=dict(
                            type='str',
                        ),
                        health_check_node_port=dict(
                            type='int',
                        ),
                        load_balancer_IP=dict(
                            type='str',
                        ),
                        load_balancer_source_ranges=dict(
                            type='list',
                            subtype='str',
                        ),
                        ports=dict(
                            type='list',
                            subtype='dict',
                            fields=dict(
                                name=dict(
                                    type='str',
                                ),
                                node_port=dict(
                                    type='int',
                                ),
                                port=dict(
                                    type='int',
                                ),
                                protocol=dict(
                                    type='str',
                                ),
                                target_port=dict(
                                    # No type specified, because this can be 'int' or 'str', and this tool
                                    # doesn't currently support setting multiple allowed types
                                ),
                            ),
                        ),
                        publish_not_ready_addresses=dict(
                            type='bool',
                        ),
                        selector=dict(
                            type='dict',
                        ),
                        session_affinity=dict(
                            type='str',
                        ),
                        session_affinity_config=dict(
                            type='dict',
                            fields=dict(
                                client_IP=dict(
                                    type='dict',
                                    fields=dict(
                                        timeout_seconds=dict(
                                            type='int',
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        type=dict(
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
            'kind': 'Service',
            'spec': dict(),
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        data['spec'] = self.build_generic(app_vars['APP']['spec'], self._plugin_config['fields']['kube_services']['spec']['fields'])

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
