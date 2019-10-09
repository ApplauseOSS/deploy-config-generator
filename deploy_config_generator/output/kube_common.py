import copy

from deploy_config_generator.utils import underscore_to_camelcase
from deploy_config_generator.output import OutputPluginBase

METADATA_FIELD_SPEC = dict(
    annotations=dict(
        type='dict',
    ),
    labels=dict(
        type='dict',
    ),
    name=dict(
        type='str',
        required=True,
    ),
    namespace=dict(
        type='str',
    ),
)

SELECTOR_FIELD_SPEC = dict(
    match_expressions=dict(
        type='list',
        subtype='dict',
        fields=dict(
            key=dict(
                type='str',
                required=True,
            ),
            operator=dict(
                type='str',
                required=True,
            ),
            values=dict(
                type='list',
                subtype='str',
                required=True,
            ),
        ),
    ),
    match_labels=dict(
        type='dict',
    ),
)

CONTAINER_FIELD_SPEC = dict(
    args=dict(
        type='list',
        subtype='str',
    ),
    command=dict(
        type='list',
        subtype='str',
    ),
    env=dict(
        type='list',
        subtype='dict',
        fields=dict(
            name=dict(
                type='str',
                required=True,
            ),
            value=dict(
                type='str',
            ),
            value_from=dict(
                type='dict',
            ),
        ),
    ),
    env_from=dict(
        type='list',
        subtype='dict',
    ),
    image=dict(
        type='str',
    ),
    image_pull_policy=dict(
        type='str',
    ),
    lifecycle=dict(
        type='dict',
    ),
    liveness_probe=dict(
        type='dict',
    ),
    name=dict(
        type='str',
    ),
    ports=dict(
        type='list',
        subtype='dict',
        fields=dict(
            container_port=dict(
                type='int',
            ),
            host_IP=dict(
                type='str',
            ),
            host_port=dict(
                type='int',
            ),
            name=dict(
                type='str',
            ),
            protocol=dict(
                type='str',
            ),
        ),
    ),
    readiness_probe=dict(
        type='dict',
    ),
    resources=dict(
        type='dict',
    ),
    security_context=dict(
        type='dict',
    ),
    stdin=dict(
        type='bool',
    ),
    stdin_once=dict(
        type='bool',
    ),
    termination_message_path=dict(
        type='str',
    ),
    termination_message_policy=dict(
        type='str',
    ),
    tty=dict(
        type='bool',
    ),
    volume_devices=dict(
        type='list',
        subtype='dict',
    ),
    volume_mounts=dict(
        type='list',
        subtype='dict',
    ),
    working_dir=dict(
        type='str',
    ),
)

POD_SPEC_FIELD_SPEC = dict(
    active_deadline_seconds=dict(
        type='int',
    ),
    affinity=dict(
        type='dict',
    ),
    automount_service_account_token=dict(
        type='bool',
    ),
    containers=dict(
        type='list',
        subtype='dict',
        fields=copy.deepcopy(CONTAINER_FIELD_SPEC),
    ),
    dns_config=dict(
        type='dict',
    ),
    dns_policy=dict(
        type='str',
    ),
    host_aliases=dict(
        type='list',
        subtype='dict',
    ),
    host_IPC=dict(
        type='bool',
    ),
    host_network=dict(
        type='bool',
    ),
    host_PID=dict(
        type='bool',
    ),
    hostname=dict(
        type='str',
    ),
    image_pull_secrets=dict(
        type='list',
        subtype='dict',
    ),
    init_containers=dict(
        type='list',
        subtype='dict',
        fields=copy.deepcopy(CONTAINER_FIELD_SPEC),
    ),
    node_name=dict(
        type='str',
    ),
    node_selector=dict(
        type='dict',
    ),
    priority=dict(
        type='int',
    ),
    priority_class_name=dict(
        type='str',
    ),
    restart_policy=dict(
        type='str',
    ),
    scheduler_name=dict(
        type='str',
    ),
    security_context=dict(
        type='dict',
    ),
    service_account_name=dict(
        type='str',
    ),
    share_process_namespace=dict(
        type='bool',
    ),
    subdomain=dict(
        type='str',
    ),
    termination_grace_period_seconds=dict(
        type='int',
    ),
    tolerations=dict(
        type='list',
        subtype='dict',
    ),
    volumes=dict(
        type='list',
        subtype='dict',
    ),
)

POD_TEMPLATE_FIELD_SPEC = dict(
    metadata=dict(
        type='dict',
        required=True,
        fields=copy.deepcopy(METADATA_FIELD_SPEC),
    ),
    spec=dict(
        type='dict',
        required=True,
        fields=copy.deepcopy(POD_SPEC_FIELD_SPEC),
    ),
)


class OutputPlugin(OutputPluginBase):

    NAME = 'kube_common'
    DESCR = 'Common class for Kubernetes plugins'

    DEFAULT_CONFIG = {
        'enabled': False,
        'fields': dict(
            dummy=dict(),
        ),
    }

    def build_generic(self, tmp_vars, fields):
        ret = dict()
        for field in fields:
            field_value = tmp_vars.get(field, None)
            value_type = None
            if isinstance(field_value, list):
                value_type = 'list'
            elif isinstance(field_value, dict):
                value_type = 'dict'
            if value_type == 'list':
                if fields[field].get('subtype', None) == 'dict' and 'fields' in fields[field]:
                    ret2 = []
                    for entry in field_value:
                        ret3 = self.build_generic(entry, fields[field]['fields'])
                        if ret3:
                            ret2.append(ret3)
                    if ret2:
                        ret[field] = ret2
                else:
                    if field_value:
                        ret[underscore_to_camelcase(field)] = field_value
            elif value_type == 'dict':
                if 'fields' in fields[field] and field_value:
                    ret2 = self.build_generic(field_value, fields[field]['fields'])
                    if ret2:
                        ret[underscore_to_camelcase(field)] = ret2
                else:
                    if field_value:
                        ret[underscore_to_camelcase(field)] = field_value
            else:
                if field_value is not None:
                    ret[underscore_to_camelcase(field)] = field_value
        return ret

    def build_metadata(self, tmp_vars):
        tmp_metadata = {}
        for field in ('name', 'labels'):
            if tmp_vars[field] is not None:
                tmp_metadata[underscore_to_camelcase(field)] = tmp_vars[field]
        return tmp_metadata

    def build_pod_template(self, tmp_vars):
        tmp_template = dict()
        tmp_template['metadata'] = self.build_metadata(tmp_vars['metadata'])
        tmp_template['spec'] = self.build_generic(tmp_vars['spec'], POD_TEMPLATE_FIELD_SPEC['spec']['fields'])
        return tmp_template