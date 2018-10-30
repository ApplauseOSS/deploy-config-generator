from deploy_config_generator.utils import json_dump
from deploy_config_generator.output import OutputPluginBase


class OutputPlugin(OutputPluginBase):

    NAME = 'marathon'
    DESCR = 'Marathon output plugin'
    FILE_EXT = '.json'

    DEFAULT_CONFIG = {
        'fields': {
            'id': dict(
                required=True,
            ),
            'image': dict(
                required=True,
            ),
            'cpus': dict(
                required=True,
            ),
            'mem': dict(
                required=True,
            ),
            'disk': dict(
                required=True,
            ),
            'instances': dict(
                default=1,
            ),
            'constraints': {},
            'ports': {},
            'env': {},
            'health_checks': {},
            'app_labels': {},
            'container_labels': {},
            'fetch': {},
            'auto_port_labels': {},
            'extra_sections': {},
        },
    }

    def is_needed(self, config):
        # We always (for now) want to output a Marathon config
        return True

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            "id": "{{ APP.id }}",
            "cpus": '{{ APP.cpus | output_float }}',
            "mem": '{{ APP.mem | output_int }}',
            "disk": '{{ APP.disk | output_int }}',
            "instances": '{{ APP.instances | output_int }}',
            # TODO: add support for container types other than 'DOCKER'
            "container": {
                "type": "DOCKER",
                "volumes": [],
                # TODO: make various attributes configurable
                "docker": {
                    "image": "{{ APP.image }}",
                    "network": "BRIDGE",
                    "privileged": False,
                    "parameters": [],
                    "forcePullImage": True
                }
            },
        }
        # Constraints
        if app_vars['APP']['constraints'] is not None:
            data['constraints'] = app_vars['APP']['constraints']
        # Ports
        self.build_port_mappings(app_vars, data)
        # Container labels
        self.build_container_labels(app_vars, data)
        # Environment
        if app_vars['APP']['env'] is not None:
            data['env'] = app_vars['APP']['env']
        # Fetch config
        self.build_fetch_config(app_vars, data)
        # Health checks
        self.build_health_checks(app_vars, data)
        # Labels
        if app_vars['APP']['app_labels'] is not None:
            data['labels'] = app_vars['APP']['app_labels']
        # Extra sections
        if app_vars['APP']['extra_sections'] is not None:
            for k, v in app_vars['APP']['extra_sections'].items():
                data[k] = v

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
            data['container']['docker']['parameters'] = container_parameters

    def build_port_mappings(self, app_vars, data):
        if app_vars['APP']['ports'] is not None:
            tmp_vars = app_vars.copy()
            port_mappings = []
            for port_index, port in enumerate(app_vars['APP']['ports']):
                tmp_vars.update(dict(port=port, port_index=port_index))
                tmp_port = {
                    "containerPort": '{{ port.container_port | output_int }}',
                    "hostPort": '{{ port.host_port | default(0) | output_int }}',
                    "servicePort": '{{ port.service_port | default(0) | output_int }}',
                    "protocol": "{{ port.protocol | default('tcp') }}",
                }
                port_labels = {}
                for label_index, label in enumerate(app_vars['APP']['auto_port_labels']):
                    tmp_vars.update(dict(label=label, label_index=label_index))
                    if not ('condition' in label) or self._template.evaluate_condition(label['condition'], tmp_vars):
                        port_labels[self._template.render_template(label['name'], tmp_vars)] = self._template.render_template(label['value'], tmp_vars)
                if port_labels:
                    tmp_port['labels'] = port_labels
                tmp_port = self._template.render_template(tmp_port, tmp_vars)
                port_mappings.append(tmp_port)
            if port_mappings:
                data['container']['docker']['portMappings'] = port_mappings

    def build_fetch_config(self, app_vars, data):
        if app_vars['APP']['fetch'] is not None:
            tmp_vars = app_vars.copy()
            fetch_config = []
            for fetch_index, fetch in enumerate(app_vars['APP']['fetch']):
                tmp_vars.update(dict(fetch=fetch, fetch_index=fetch_index))
                if not ('condition' in fetch) or self._template.evaluate_condition(fetch['condition'], tmp_vars):
                    tmp_fetch = {}
                    tmp_fetch.update(fetch)
                    if 'condition' in tmp_fetch:
                        del tmp_fetch['condition']
                    fetch_config.append(tmp_fetch)
            if fetch_config:
                data['fetch'] = fetch_config

    def build_health_checks(self, app_vars, data):
        health_checks_config = []
        health_checks = []
        # Health checks from ports
        if app_vars['APP']['ports'] is not None:
            for port_index, port in enumerate(app_vars['APP']['ports']):
                if 'health_check' in port:
                    health_checks.append(port['health_check'])
                    health_checks[-1]['port_index'] = port_index
        # Other health checks
        if app_vars['APP']['health_checks'] is not None:
            health_checks.extend(app_vars['APP']['health_checks'])
        for check_index, check in enumerate(health_checks):
            # TODO: make these parameters configurable
            tmp_check = {
                "gracePeriodSeconds": 30,
                "intervalSeconds": 5,
                "timeoutSeconds": 10,
                "maxConsecutiveFailures": 10
            }
            if 'endpoint' in check:
                tmp_check.update(dict(
                    path=check['endpoint'],
                    protocol=(check['type'] if 'type' in check else 'MESOS_HTTP'),
                    portIndex=check['port_index']
                ))
            elif 'command' in check:
                tmp_check.update(dict(
                    protocol='COMMAND',
                    command=dict(
                        value=check['command']
                    )
                ))
            health_checks_config.append(tmp_check)
        if health_checks_config:
            data['healthChecks'] = health_checks_config
