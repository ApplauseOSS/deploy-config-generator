import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_dnsendpoint'
    DESCR = 'Kubernetes external-dns DNSEndpoint output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_dnsendpoints': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    required=True,
                    fields=dict(
                        endpoints=dict(
                            type='list',
                            subtype='dict',
                            required=True,
                            fields=dict(
                                dns_name=dict(
                                    type='str',
                                ),
                                labels=dict(
                                    type='dict',
                                ),
                                provider_specific=dict(
                                    type='list',
                                    subtype='dict',
                                    fields=dict(
                                        name=dict(
                                            type='str',
                                        ),
                                        value=dict(
                                            type='str',
                                        ),
                                    ),
                                ),
                                record_TTL=dict(
                                    type='int',
                                ),
                                record_type=dict(
                                    type='str',
                                ),
                                targets=dict(
                                    type='list',
                                    subtype='str',
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
            'apiVersion': 'externaldns.k8s.io/v1alpha1',
            'kind': 'DNSEndpoint',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        data['spec'] = self.build_generic(app_vars['APP']['spec'], self._fields['kube_dnsendpoints']['spec']['fields'])

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
