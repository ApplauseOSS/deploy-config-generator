import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_kong_ingress'
    DESCR = 'Kubernetes KongIngress output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kong_ingresses': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                upstream=dict(
                    type='dict',
                    fields=dict(
                        slots=dict(
                            type='int',
                        ),
                        hash_on=dict(
                            type='str',
                        ),
                        hash_fallback=dict(
                            type='str',
                        ),
                        healthchecks=dict(
                            type='dict',
                            fields=dict(
                                active=dict(
                                    type='dict',
                                    fields=dict(
                                        concurrency=dict(
                                            type='int',
                                        ),
                                        healthy=dict(
                                            type='dict',
                                            fields=dict(
                                                http_statuses=dict(
                                                    type='list',
                                                    subtype='int',
                                                ),
                                                interval=dict(
                                                    type='int',
                                                ),
                                                successes=dict(
                                                    type='int',
                                                ),
                                            ),
                                        ),
                                        http_path=dict(
                                            type='str',
                                        ),
                                        timeout=dict(
                                            type='int',
                                        ),
                                        unhealthy=dict(
                                            type='dict',
                                            fields=dict(
                                                http_failures=dict(
                                                    type='int',
                                                ),
                                                http_statuses=dict(
                                                    type='list',
                                                    subtype='int',
                                                ),
                                                interval=dict(
                                                    type='int',
                                                ),
                                                tcp_failures=dict(
                                                    type='int',
                                                ),
                                                timeouts=dict(
                                                    type='int',
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                                passive=dict(
                                    type='dict',
                                    fields=dict(
                                        healthy=dict(
                                            type='dict',
                                            fields=dict(
                                                http_statuses=dict(
                                                    type='list',
                                                    subtype='int',
                                                ),
                                                successes=dict(
                                                    type='int',
                                                ),
                                            ),
                                        ),
                                        unhealthy=dict(
                                            type='dict',
                                            fields=dict(
                                                http_failures=dict(
                                                    type='int',
                                                ),
                                                http_statuses=dict(
                                                    type='list',
                                                    subtype='int',
                                                ),
                                                tcp_failures=dict(
                                                    type='int',
                                                ),
                                                timeouts=dict(
                                                    type='int',
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                proxy=dict(
                    type='dict',
                    fields=dict(
                        protocol=dict(
                            type='str',
                        ),
                        path=dict(
                            type='str',
                        ),
                        retries=dict(
                            type='int',
                        ),
                        connect_timeout=dict(
                            type='int',
                        ),
                        read_timeout=dict(
                            type='int',
                        ),
                        write_timeout=dict(
                            type='int',
                        ),
                    ),
                ),
                route=dict(
                    type='dict',
                    fields=dict(
                        methods=dict(
                            type='list',
                            subtype='str',
                        ),
                        regex_priority=dict(
                            type='int',
                        ),
                        strip_path=dict(
                            type='bool',
                        ),
                        preserve_host=dict(
                            type='bool',
                        ),
                        protocols=dict(
                            type='list',
                            subtype='str',
                        ),
                        path_handling=dict(
                            type='str',
                        ),
                        https_redirect_status_code=dict(
                            type='int',
                        ),
                    ),
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'configuration.konghq.com/v1',
            'kind': 'KongIngress',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        for field in ('upstream', 'proxy', 'route'):
            if app_vars['APP'][field]:
                data.update(self.build_generic(app_vars['APP'], {field: self._fields['kong_ingresses'][field]}, camel_case=False))

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
