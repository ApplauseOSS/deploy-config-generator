from deploy_config_generator.utils import json_dump, underscore_to_camelcase
from deploy_config_generator.output import OutputPluginBase


class OutputPlugin(OutputPluginBase):

    NAME = 'marathon'
    DESCR = 'Marathon output plugin'
    FILE_EXT = '.json'

    DEFAULT_CONFIG = {
        'fields': {
            'apps': {
                'id': dict(
                    required=True,
                    description='Unique ID for app in Marathon',
                ),
                'image': dict(
                    required=True,
                    description='Docker image to use',
                ),
                'cpus': dict(
                    type='float',
                    required=True,
                ),
                'mem': dict(
                    type='float',
                    required=True,
                ),
                'disk': dict(
                    required=True,
                    type='int',
                ),
                'instances': dict(
                    default=1,
                    type='int',
                ),
                'constraints': dict(
                    type='list',
                ),
                'args': dict(
                    type='list',
                    description='Arguments to pass to container',
                ),
                'accepted_resource_roles': dict(
                    type='list',
                ),
                'ports': dict(
                    description='List of port definitions',
                    type='list',
                    subtype='dict',
                    fields=dict(
                        container_port=dict(
                            type='int',
                            required=True,
                            description='Port that the service is listening on inside the container',
                        ),
                        host_port=dict(
                            type='int',
                            default=0,
                        ),
                        service_port=dict(
                            type='int',
                            default=0,
                        ),
                        protocol=dict(
                            type='str',
                            default='tcp',
                        ),
                        labels=dict(
                            description='List of label name/value pairs to apply to port',
                            type='list',
                            subtype='dict',
                            fields=dict(
                                name={},
                                value={},
                                condition=dict(
                                    description=('Condition to evaluate before applying label. The vars `port` (current port definition) '
                                                 'and `port_index` (index of current port definition in list) are available'),
                                ),
                            ),
                        ),
                    ),
                ),
                'port_definitions': dict(
                    description='List of port definitions (for HOST networking mode)',
                    type='list',
                    subtype='dict',
                    fields=dict(
                        port=dict(
                            type='int',
                            required=True,
                        ),
                        protocol=dict(
                            type='str',
                        ),
                        name=dict(
                            type='str',
                        ),
                        labels=dict(
                            description='List of label name/value pairs to apply to port',
                            type='list',
                            subtype='dict',
                            fields=dict(
                                name={},
                                value={},
                                condition=dict(
                                    description=('Condition to evaluate before applying label. The vars `port` (current port definition) '
                                                 'and `port_index` (index of current port definition in list) are available'),
                                ),
                            ),
                        ),
                    ),
                ),
                'require_ports': dict(
                    description='Whether to require that ports specified in `port_definitions` are available (for HOST networking mode)',
                    type='bool',
                ),
                'cmd': dict(
                    description='Command to execute (optional)',
                ),
                'env': dict(
                    description='Environment variables to pass to the container',
                    type='dict',
                ),
                'secrets': dict(
                    description='List of secrets from the DC/OS secret store',
                    type='list',
                    subtype='dict',
                    fields=dict(
                        name=dict(
                            required=True,
                            description='Name of secret to expose for env/volumes',
                        ),
                        source=dict(
                            required=True,
                            description='Name of secret in DC/OS secret store',
                        ),
                    ),
                ),
                'health_checks': dict(
                    type='list',
                    subtype='dict',
                    fields=dict(
                        port_index=dict(
                            type='int',
                        ),
                        port=dict(
                            type='int',
                        ),
                        protocol=dict(
                            default='MESOS_HTTP',
                        ),
                        grace_period_seconds=dict(
                            type='int',
                        ),
                        interval_seconds=dict(
                            type='int',
                        ),
                        timeout_seconds=dict(
                            type='int',
                        ),
                        delay_seconds=dict(
                            type='int',
                        ),
                        max_consecutive_failures=dict(
                            type='int',
                        ),
                        command=dict(
                            type='str',
                        ),
                        path=dict(
                            type='str',
                        ),
                    ),
                ),
                'labels': dict(
                    type='dict',
                ),
                'container_labels': dict(
                    type='list',
                ),
                'fetch': dict(
                    type='list',
                    subtype='dict',
                    fields=dict(
                        uri=dict(
                            type='str',
                        ),
                        executable=dict(
                            type='bool',
                        ),
                        extract=dict(
                            type='bool',
                        ),
                        cache=dict(
                            type='bool',
                        ),
                        condition=dict(
                            description=('Condition to evaluate before applying fetch config. The vars `fetch` (current fetch definition) '
                                         'and `fetch_index` (index of current fetch defintion in list) are available'),
                        ),
                    ),
                ),
                'upgrade_strategy': dict(
                    type='dict',
                    fields=dict(
                        minimum_health_capacity=dict(
                            type='float',
                        ),
                        maximum_over_capacity=dict(
                            type='float',
                        ),
                    ),
                ),
                'unreachable_strategy': dict(
                    type='dict',
                    fields=dict(
                        inactive_after_seconds=dict(
                            type='int',
                        ),
                        expunge_after_seconds=dict(
                            type='int',
                        ),
                    ),
                ),
                'docker_network': dict(
                    default='BRIDGE',
                ),
                'networks': dict(
                    type='list',
                    description='List of networks. This param overrides the "docker_network" param',
                    subtype='dict',
                    fields=dict(
                        name=dict(
                            type='str',
                        ),
                        mode=dict(
                            type='str',
                            required=True,
                        ),
                        labels=dict(
                            type='dict',
                        ),
                    ),
                ),
                'docker_privileged': dict(
                    type='bool',
                    default=False,
                ),
                'docker_parameters': dict(
                    type='list',
                    subtype='dict',
                    fields=dict(
                        key=dict(
                            type='str'
                        ),
                        value=dict(
                            type='str'
                        ),
                    ),
                ),
                'volumes': dict(
                    type='list',
                    subtype='dict',
                    fields=dict(
                        container_path=dict(
                            type='str',
                        ),
                        host_path=dict(
                            type='str',
                        ),
                        mode=dict(
                            type='str',
                        ),
                        persistent=dict(
                            type='dict',
                            fields=dict(
                                type=dict(
                                    type='str',
                                ),
                                size=dict(
                                    type='float',
                                ),
                                profile_name=dict(
                                    type='str',
                                ),
                                max_size=dict(
                                    type='float',
                                ),
                                constraints=dict(
                                    type='list',
                                ),
                            ),
                        ),
                    ),
                ),
            }
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            "id": app_vars['APP']['id'],
            "cpus": app_vars['APP']['cpus'],
            "mem": app_vars['APP']['mem'],
            "disk": app_vars['APP']['disk'],
            "instances": app_vars['APP']['instances'],
            # TODO: add support for container types other than 'DOCKER'
            "container": {
                "type": "DOCKER",
                "volumes": [],
                # TODO: make various attributes configurable
                "docker": {
                    "image": app_vars['APP']['image'],
                    "privileged": app_vars['APP']['docker_privileged'],
                    "parameters": app_vars['APP']['docker_parameters'],
                    "forcePullImage": True
                }
            },
        }
        # Constraints
        if app_vars['APP']['constraints']:
            data['constraints'] = app_vars['APP']['constraints']
        # Ports
        self.build_port_mappings(app_vars, data)
        self.build_port_definitions(app_vars, data)
        # Container labels
        self.build_container_labels(app_vars, data)
        # Networks
        self.build_networks(app_vars, data)
        # Volumes
        self.build_volumes(app_vars, data)
        # Environment
        if app_vars['APP']['env'] is not None:
            data['env'] = app_vars['APP']['env']
        # Secrets
        self.build_secrets(app_vars, data)
        # Fetch config
        self.build_fetch_config(app_vars, data)
        # Health checks
        self.build_health_checks(app_vars, data)
        # Upgrade/unreachable strategies
        self.build_upgrade_strategy(app_vars, data)
        self.build_unreachable_strategy(app_vars, data)
        # Misc attributes
        for field in ('labels', 'args', 'cmd', 'accepted_resource_roles'):
            if app_vars['APP'][field]:
                data[underscore_to_camelcase(field)] = app_vars['APP'][field]

        output = json_dump(self._template.render_template(data, app_vars))
        return output

    def build_container_labels(self, app_vars, data):
        if app_vars['APP']['container_labels'] is not None:
            container_parameters = []
            for label_index, label in enumerate(app_vars['APP']['container_labels']):
                tmp_param = {
                    "key": "label",
                    "value": label
                }
                container_parameters.append(tmp_param)
            data['container']['docker']['parameters'] += container_parameters

    def build_secrets(self, app_vars, data):
        if app_vars['APP']['secrets']:
            secrets = {}
            tmp_vars = app_vars.copy()
            for secret_index, secret in enumerate(app_vars['APP']['secrets']):
                tmp_vars.update(dict(secret=secret, secret_index=secret_index))
                tmp_secret = {
                    'source': secret['source']
                }
                if tmp_secret:
                    tmp_secret = self._template.render_template(tmp_secret, tmp_vars)
                    secrets[secret['name']] = tmp_secret
            if secrets:
                data['secrets'] = secrets

    def build_networks(self, app_vars, data):
        networks = []
        # The 'networks' param overrides the 'docker_network' param, so look for it first
        if app_vars['APP']['networks']:
            for net in app_vars['APP']['networks']:
                networks.append(net)
        else:
            # Translate 'docker_network' value to new-style network
            tmp_network = {}
            if app_vars['APP']['docker_network'].lower() == 'bridge':
                tmp_network['mode'] = 'container/bridge'
            elif app_vars['APP']['docker_network'].lower() == 'host':
                tmp_network['mode'] = 'host'
            else:
                # TODO: do something meaningful for unknown network mode
                pass
            networks.append(tmp_network)
        data['networks'] = networks

    def build_volumes(self, app_vars, data):
        if app_vars['APP']['volumes']:
            volumes = []
            for volume_index, volume in enumerate(app_vars['APP']['volumes']):
                tmp_volume = {}
                for field in ('container_path', 'host_path', 'mode'):
                    if volume[field] is not None:
                        tmp_volume[underscore_to_camelcase(field)] = volume[field]
                if volume['persistent']:
                    tmp_persistent = {}
                    for field in ('type', 'size', 'profile_name', 'max_size'):
                        if volume['persistent'][field] is not None:
                            tmp_persistent[underscore_to_camelcase(field)] = volume['persistent'][field]
                    if volume['persistent']['constraints']:
                        tmp_persistent['constraints'] = volume['persistent']['constraints']
                    if tmp_persistent:
                        tmp_volume['persistent'] = tmp_persistent
                volumes.append(tmp_volume)
            data['container']['volumes'] = volumes

    def build_port_mappings(self, app_vars, data):
        port_mappings = []
        tmp_vars = app_vars.copy()
        for port_index, port in enumerate(app_vars['APP']['ports']):
            tmp_vars.update(dict(port=port, port_index=port_index))
            tmp_port = {
                "protocol": port['protocol'],
            }
            for field in ('container_port', 'host_port', 'service_port'):
                if port[field] is not None:
                    tmp_port[underscore_to_camelcase(field)] = int(port[field])
            # Port labels
            port_labels = {}
            for label_index, label in enumerate(port['labels']):
                tmp_vars.update(dict(label=label, label_index=label_index))
                if label['condition'] is None or self._template.evaluate_condition(label['condition'], tmp_vars):
                    port_labels[self._template.render_template(label['name'], tmp_vars)] = self._template.render_template(label['value'], tmp_vars)
            if port_labels:
                tmp_port['labels'] = port_labels
            # Render templates now so that loop vars can be used
            tmp_port = self._template.render_template(tmp_port, tmp_vars)
            port_mappings.append(tmp_port)
        if port_mappings:
            data['container']['docker']['portMappings'] = port_mappings

    def build_port_definitions(self, app_vars, data):
        port_definitions = []
        tmp_vars = app_vars.copy()
        for port_index, port in enumerate(app_vars['APP']['port_definitions']):
            tmp_vars.update(dict(port=port, port_index=port_index))
            tmp_port = {
                "port": int(port['port']),
            }
            for field in ('name', 'protocol'):
                if port[field] is not None:
                    tmp_port[underscore_to_camelcase(field)] = port[field]
            # Port labels
            port_labels = {}
            for label_index, label in enumerate(port['labels']):
                tmp_vars.update(dict(label=label, label_index=label_index))
                if label['condition'] is None or self._template.evaluate_condition(label['condition'], tmp_vars):
                    port_labels[self._template.render_template(label['name'], tmp_vars)] = self._template.render_template(label['value'], tmp_vars)
            if port_labels:
                tmp_port['labels'] = port_labels
            # Render templates now so that loop vars can be used
            tmp_port = self._template.render_template(tmp_port, tmp_vars)
            port_definitions.append(tmp_port)
        if port_definitions:
            data['portDefinitions'] = port_definitions
        if app_vars['APP']['require_ports'] is not None:
            data['requirePorts'] = app_vars['APP']['require_ports']

    def build_fetch_config(self, app_vars, data):
        fetch_config = []
        tmp_vars = app_vars.copy()
        for fetch_index, fetch in enumerate(app_vars['APP']['fetch']):
            tmp_vars.update(dict(fetch=fetch, fetch_index=fetch_index))
            if fetch['condition'] is None or self._template.evaluate_condition(fetch['condition'], tmp_vars):
                tmp_fetch = {}
                for field in ('uri', 'executable', 'cache', 'extract'):
                    if fetch[field] is not None:
                        tmp_fetch[field] = fetch[field]
                fetch_config.append(tmp_fetch)
        if fetch_config:
            data['fetch'] = fetch_config

    def build_health_checks(self, app_vars, data):
        health_checks = []
        tmp_vars = app_vars.copy()
        for check_index, check in enumerate(app_vars['APP']['health_checks']):
            tmp_vars.update(dict(check=check, check_index=check_index))
            tmp_check = {}
            for field in ('grace_period_seconds', 'interval_seconds', 'timeout_seconds', 'delay_seconds',
                          'max_consecutive_failures', 'path', 'port_index', 'port', 'protocol'):
                if check[field] is not None:
                    tmp_check[underscore_to_camelcase(field)] = check[field]
            if check['command'] is not None:
                tmp_check.update(dict(
                    protocol='COMMAND',
                    command=dict(
                        value=check['command']
                    )
                ))
            # Render templates now so that loop vars can be used
            tmp_check = self._template.render_template(tmp_check, tmp_vars)
            health_checks.append(tmp_check)
        if health_checks:
            data['healthChecks'] = health_checks

    def build_upgrade_strategy(self, app_vars, data):
        strategy = {}
        app_vars_section = app_vars['APP']['upgrade_strategy']
        for field in ('minimum_health_capacity', 'maximum_over_capacity'):
            if app_vars_section[field] is not None:
                strategy[underscore_to_camelcase(field)] = float(app_vars_section[field])
        if strategy:
            data['upgradeStrategy'] = strategy

    def build_unreachable_strategy(self, app_vars, data):
        strategy = {}
        app_vars_section = app_vars['APP']['unreachable_strategy']
        for field in ('inactive_after_seconds', 'expunge_after_seconds'):
            if app_vars_section[field] is not None:
                strategy[underscore_to_camelcase(field)] = int(app_vars_section[field])
        if strategy:
            data['unreachableStrategy'] = strategy
