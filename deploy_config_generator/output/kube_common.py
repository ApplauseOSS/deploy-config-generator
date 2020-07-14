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

EXEC_ACTION_FIELD_SPEC = dict(
    command=dict(
        type='list',
        subtype='str',
    ),
)

HTTP_GET_ACTION_FIELD_SPEC = dict(
    host=dict(
        type='str',
    ),
    http_headers=dict(
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
    path=dict(
        type='str',
    ),
    port=dict(
        # This can be either int or str, so we don't set a type
    ),
    scheme=dict(
        type='str',
    ),
)

TCP_SOCKET_ACTION_FIELD_SPEC = dict(
    host=dict(
        type='str',
    ),
    port=dict(
        # This can be either int or str, so we don't set a type
    ),
)

# We use the { ... } syntax for this dict because 'exec' can't be used as a bareword in py27
PROBE_FIELD_SPEC = {
    'exec': dict(
        type='dict',
        fields=copy.deepcopy(EXEC_ACTION_FIELD_SPEC),
    ),
    'failure_threshold': dict(
        type='int',
    ),
    'http_get': dict(
        type='dict',
        fields=copy.deepcopy(HTTP_GET_ACTION_FIELD_SPEC),
    ),
    'initial_delay_seconds': dict(
        type='int',
    ),
    'period_seconds': dict(
        type='int',
    ),
    'success_threshold': dict(
        type='int',
    ),
    'tcp_socket': dict(
        type='dict',
        fields=copy.deepcopy(TCP_SOCKET_ACTION_FIELD_SPEC),
    ),
    'timeout_seconds': dict(
        type='int',
    ),
}

# We use the { ... } syntax for this dict because 'exec' can't be used as a bareword in py27
LIFECYCLE_HANDLER_FIELD_SPEC = {
    'exec': dict(
        type='dict',
        fields=copy.deepcopy(EXEC_ACTION_FIELD_SPEC),
    ),
    'http_get': dict(
        type='dict',
        fields=copy.deepcopy(HTTP_GET_ACTION_FIELD_SPEC),
    ),
    'tcp_socket': dict(
        type='dict',
        fields=copy.deepcopy(TCP_SOCKET_ACTION_FIELD_SPEC),
    ),
}

SELINUX_OPTIONS_FIELD_SPEC = dict(
    level=dict(
        type='str',
    ),
    role=dict(
        type='str',
    ),
    type=dict(
        type='str',
    ),
    user=dict(
        type='str',
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
                fields=dict(
                    config_map_key_ref=dict(
                        type='dict',
                        fields=dict(
                            key=dict(
                                type='str',
                                required=True,
                            ),
                            name=dict(
                                type='str',
                                required=True,
                            ),
                            optional=dict(
                                type='bool',
                            ),
                        ),
                    ),
                    field_ref=dict(
                        type='dict',
                        fields=dict(
                            api_version=dict(
                                type='str',
                            ),
                            field_path=dict(
                                type='str',
                                required=True,
                            ),
                        ),
                    ),
                    resource_field_ref=dict(
                        type='dict',
                        fields=dict(
                            container_name=dict(
                                type='str',
                            ),
                            divisor=dict(
                                # This field can have multiple types (int or str), so we set none
                            ),
                            resource=dict(
                                type='str',
                                required=True,
                            ),
                        ),
                    ),
                    secret_key_ref=dict(
                        type='dict',
                        fields=dict(
                            key=dict(
                                type='str',
                                required=True,
                            ),
                            name=dict(
                                type='str',
                                required=True,
                            ),
                            optional=dict(
                                type='bool',
                            ),
                        ),
                    ),
                ),
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
        fields=dict(
            pre_stop=dict(
                type='dict',
                fields=copy.deepcopy(LIFECYCLE_HANDLER_FIELD_SPEC),
            ),
            post_start=dict(
                type='dict',
                fields=copy.deepcopy(LIFECYCLE_HANDLER_FIELD_SPEC),
            ),
        ),
    ),
    liveness_probe=dict(
        type='dict',
        fields=copy.deepcopy(PROBE_FIELD_SPEC),
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
        fields=copy.deepcopy(PROBE_FIELD_SPEC),
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
    security_context=dict(
        type='dict',
        fields=dict(
            allow_privilege_escalation=dict(
                type='bool',
            ),
            capabilities=dict(
                type='dict',
                fields=dict(
                    add=dict(
                        type='list',
                        subtype='str',
                    ),
                    drop=dict(
                        type='list',
                        substype='str',
                    ),
                ),
            ),
            privileged=dict(
                type='bool',
            ),
            proc_mount=dict(
                type='str',
            ),
            read_only_root_filesystem=dict(
                type='bool',
            ),
            run_as_group=dict(
                type='int',
            ),
            run_as_non_root=dict(
                type='bool',
            ),
            run_as_user=dict(
                type='int',
            ),
            selinux_options=dict(
                type='dict',
                fields=copy.deepcopy(SELINUX_OPTIONS_FIELD_SPEC),
            ),
        ),
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
        fields=dict(
            fs_group=dict(
                type='int',
            ),
            run_as_group=dict(
                type='int',
            ),
            run_as_non_root=dict(
                type='bool',
            ),
            run_as_user=dict(
                type='int',
            ),
            selinux_options=dict(
                type='dict',
                fields=copy.deepcopy(SELINUX_OPTIONS_FIELD_SPEC),
            ),
            supplemental_groups=dict(
                type='list',
                subtype='int',
            ),
            sysctls=dict(
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
        ),
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
        fields=copy.deepcopy(METADATA_FIELD_SPEC),
    ),
    spec=dict(
        type='dict',
        required=True,
        fields=copy.deepcopy(POD_SPEC_FIELD_SPEC),
    ),
)

JOB_SPEC_FIELD_SPEC = dict(
    active_deadline_seconds=dict(
        type='int',
    ),
    backoff_limit=dict(
        type='int',
    ),
    completions=dict(
        type='int',
    ),
    manual_selector=dict(
        type='bool',
    ),
    parallelism=dict(
        type='int',
    ),
    selector=dict(
        type='dict',
        fields=copy.deepcopy(SELECTOR_FIELD_SPEC),
    ),
    template=dict(
        type='dict',
        required=True,
        fields=copy.deepcopy(POD_TEMPLATE_FIELD_SPEC),
    ),
    ttl_seconds_after_finished=dict(
        type='int',
    ),
)

PERSISTENT_VOLUME_CLAIM_FIELD_SPEC = dict(
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
        fields=copy.deepcopy(SELECTOR_FIELD_SPEC),
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

    def build_generic(self, tmp_vars, fields, camel_case=True, debug=False):
        if debug:
            print('build_generic(): tmp_vars=%s, fields=%s' % (tmp_vars, fields))
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
                        ret3 = self.build_generic(entry, fields[field]['fields'], camel_case=camel_case, debug=debug)
                        if ret3:
                            ret2.append(ret3)
                    if ret2:
                        ret[(underscore_to_camelcase(field) if camel_case else field)] = ret2
                else:
                    if field_value:
                        ret[(underscore_to_camelcase(field) if camel_case else field)] = field_value
            elif value_type == 'dict':
                if fields[field].get('fields', None) and field_value:
                    ret2 = self.build_generic(field_value, fields[field]['fields'], camel_case=camel_case, debug=debug)
                    if ret2:
                        ret[(underscore_to_camelcase(field) if camel_case else field)] = ret2
                else:
                    if field_value:
                        ret[(underscore_to_camelcase(field) if camel_case else field)] = field_value
            else:
                if field_value is not None:
                    ret[(underscore_to_camelcase(field) if camel_case else field)] = field_value
        return ret

    def build_metadata(self, tmp_vars):
        tmp_metadata = {}
        for field in ('annotations', 'labels', 'name', 'namespace'):
            if tmp_vars[field] is not None:
                tmp_metadata[underscore_to_camelcase(field)] = tmp_vars[field]
        return tmp_metadata

    def build_pod_template(self, tmp_vars):
        tmp_template = dict()
        tmp_template['metadata'] = self.build_metadata(tmp_vars['metadata'])
        tmp_template['spec'] = self.build_generic(tmp_vars['spec'], POD_TEMPLATE_FIELD_SPEC['spec']['fields'])
        return tmp_template
