import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


INGRESS_BACKEND_FIELD_SPEC = dict(
    resource=dict(
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
    service=dict(
        type='dict',
        fields=dict(
            name=dict(
                type='str',
            ),
            port=dict(
                type='dict',
                fields=dict(
                    name=dict(
                        type='str',
                    ),
                    number=dict(
                        type='int',
                    ),
                ),
            ),
        ),
    ),
)


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_ingress'
    DESCR = 'Kubernetes ingress output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_ingresses': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    required=True,
                    fields=dict(
                        default_backend=dict(
                            type='dict',
                            fields=copy.deepcopy(INGRESS_BACKEND_FIELD_SPEC),
                        ),
                        rules=dict(
                            type='list',
                            subtype='dict',
                            fields=dict(
                                host=dict(
                                    type='str',
                                ),
                                http=dict(
                                    type='dict',
                                    fields=dict(
                                        paths=dict(
                                            type='list',
                                            subtype='dict',
                                            fields=dict(
                                                backend=dict(
                                                    type='dict',
                                                    fields=copy.deepcopy(INGRESS_BACKEND_FIELD_SPEC),
                                                ),
                                                path=dict(
                                                    type='str',
                                                ),
                                                path_type=dict(
                                                    type='str',
                                                    required=True,
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        tls=dict(
                            type='list',
                            subtype='dict',
                            fields=dict(
                                host=dict(
                                    type='list',
                                    subtype='str',
                                ),
                                secret_name=dict(
                                    type='str',
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
            'apiVersion': 'networking.k8s.io/v1',
            'kind': 'Ingress',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        data['spec'] = self.build_generic(app_vars['APP']['spec'], self._fields['kube_ingresses']['spec']['fields'])

        data = self._template.render_template(data, app_vars)
        output = yaml_dump(data)
        return (output, self.get_output_filename_suffix(data))
