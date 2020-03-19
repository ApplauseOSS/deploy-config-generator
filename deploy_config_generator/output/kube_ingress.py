import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


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
                        backend=dict(
                            type='dict',
                            fields=dict(
                                service_name=dict(
                                    type='str',
                                ),
                                service_port=dict(
                                    # The port can be a string or an int, so we don't specify a type
                                ),
                            ),
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
                                                    fields=dict(
                                                        service_name=dict(
                                                            type='str',
                                                        ),
                                                        service_port=dict(
                                                            # The port can be a string or an int, so we don't specify the type
                                                        ),
                                                    ),
                                                ),
                                                path=dict(
                                                    type='str',
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
            'apiVersion': 'extensions/v1beta1',
            'kind': 'Ingress',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        data['spec'] = self.build_generic(app_vars['APP']['spec'], self._fields['kube_ingresses']['spec']['fields'])

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
