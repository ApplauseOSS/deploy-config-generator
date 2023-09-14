<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_statefulset

Kubernetes statefulset output plugin

### Parameters


#### Deploy config section: kube_statefulsets

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`spec`|`dict`|yes||
`spec . pod_management_policy`|`str`|no||
`spec . replicas`|`int`|no||
`spec . revision_history_limit`|`int`|no||
`spec . selector`|`dict`|yes||
`spec . selector . match_expressions`|`list` (of `dict`)|no||
`spec . selector . match_expressions . key`|`str`|yes||
`spec . selector . match_expressions . operator`|`str`|yes||
`spec . selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . selector . match_labels`|`dict`|no||
`spec . service_name`|`str`|yes||
`spec . template`|`dict`|yes||
`spec . template . metadata`|`dict`|no||
`spec . template . metadata . annotations`|`dict`|no||
`spec . template . metadata . labels`|`dict`|no||
`spec . template . metadata . name`|`str`|no||
`spec . template . metadata . namespace`|`str`|no||
`spec . template . spec`|`dict`|yes||
`spec . template . spec . active_deadline_seconds`|`int`|no||
`spec . template . spec . affinity`|`dict`|no||
`spec . template . spec . affinity . node_affinity`|`dict`|no||
`spec . template . spec . affinity . pod_affinity`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_expressions`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_expressions . key`|`str`|yes||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_expressions . operator`|`str`|yes||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_labels`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . namespaces`|`list` (of `str`)|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_expressions`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_expressions . key`|`str`|yes||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_expressions . operator`|`str`|yes||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_labels`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . topology_key`|`str`|no||
`spec . template . spec . affinity . pod_affinity . preferred_during_scheduling_ignored_during_execution . weight`|`int`|no||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . label_selector`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_expressions`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_expressions . key`|`str`|yes||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_expressions . operator`|`str`|yes||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_labels`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . namespaces`|`list` (of `str`)|no||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . node_selector`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_expressions`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_expressions . key`|`str`|yes||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_expressions . operator`|`str`|yes||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_labels`|`dict`|no||
`spec . template . spec . affinity . pod_affinity . required_during_scheduling_ignored_during_execution . topology_key`|`str`|no||
`spec . template . spec . affinity . pod_anti_affinity`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_expressions`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_expressions . key`|`str`|yes||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_expressions . operator`|`str`|yes||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . label_selector . match_labels`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . namespaces`|`list` (of `str`)|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_expressions`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_expressions . key`|`str`|yes||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_expressions . operator`|`str`|yes||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . node_selector . match_labels`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . pod_affinity_term . topology_key`|`str`|no||
`spec . template . spec . affinity . pod_anti_affinity . preferred_during_scheduling_ignored_during_execution . weight`|`int`|no||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . label_selector`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_expressions`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_expressions . key`|`str`|yes||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_expressions . operator`|`str`|yes||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . label_selector . match_labels`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . namespaces`|`list` (of `str`)|no||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . node_selector`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_expressions`|`list` (of `dict`)|no||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_expressions . key`|`str`|yes||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_expressions . operator`|`str`|yes||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . node_selector . match_labels`|`dict`|no||
`spec . template . spec . affinity . pod_anti_affinity . required_during_scheduling_ignored_during_execution . topology_key`|`str`|no||
`spec . template . spec . automount_service_account_token`|`bool`|no||
`spec . template . spec . containers`|`list` (of `dict`)|no||
`spec . template . spec . containers . args`|`list` (of `str`)|no||
`spec . template . spec . containers . command`|`list` (of `str`)|no||
`spec . template . spec . containers . env`|`list` (of `dict`)|no||
`spec . template . spec . containers . env . name`|`str`|yes||
`spec . template . spec . containers . env . value`|`str`|no||
`spec . template . spec . containers . env . value_from`|`dict`|no||
`spec . template . spec . containers . env . value_from . config_map_key_ref`|`dict`|no||
`spec . template . spec . containers . env . value_from . config_map_key_ref . key`|`str`|yes||
`spec . template . spec . containers . env . value_from . config_map_key_ref . name`|`str`|yes||
`spec . template . spec . containers . env . value_from . config_map_key_ref . optional`|`bool`|no||
`spec . template . spec . containers . env . value_from . field_ref`|`dict`|no||
`spec . template . spec . containers . env . value_from . field_ref . api_version`|`str`|no||
`spec . template . spec . containers . env . value_from . field_ref . field_path`|`str`|yes||
`spec . template . spec . containers . env . value_from . resource_field_ref`|`dict`|no||
`spec . template . spec . containers . env . value_from . resource_field_ref . container_name`|`str`|no||
`spec . template . spec . containers . env . value_from . resource_field_ref . divisor`||no||
`spec . template . spec . containers . env . value_from . resource_field_ref . resource`|`str`|yes||
`spec . template . spec . containers . env . value_from . secret_key_ref`|`dict`|no||
`spec . template . spec . containers . env . value_from . secret_key_ref . key`|`str`|yes||
`spec . template . spec . containers . env . value_from . secret_key_ref . name`|`str`|yes||
`spec . template . spec . containers . env . value_from . secret_key_ref . optional`|`bool`|no||
`spec . template . spec . containers . env_from`|`list` (of `dict`)|no||
`spec . template . spec . containers . image`|`str`|no||
`spec . template . spec . containers . image_pull_policy`|`str`|no||
`spec . template . spec . containers . lifecycle`|`dict`|no||
`spec . template . spec . containers . lifecycle . post_start`|`dict`|no||
`spec . template . spec . containers . lifecycle . post_start . exec`|`dict`|no||
`spec . template . spec . containers . lifecycle . post_start . exec . command`|`list` (of `str`)|no||
`spec . template . spec . containers . lifecycle . post_start . http_get`|`dict`|no||
`spec . template . spec . containers . lifecycle . post_start . http_get . host`|`str`|no||
`spec . template . spec . containers . lifecycle . post_start . http_get . http_headers`|`list` (of `dict`)|no||
`spec . template . spec . containers . lifecycle . post_start . http_get . http_headers . name`|`str`|no||
`spec . template . spec . containers . lifecycle . post_start . http_get . http_headers . value`|`str`|no||
`spec . template . spec . containers . lifecycle . post_start . http_get . path`|`str`|no||
`spec . template . spec . containers . lifecycle . post_start . http_get . port`||no||
`spec . template . spec . containers . lifecycle . post_start . http_get . scheme`|`str`|no||
`spec . template . spec . containers . lifecycle . post_start . tcp_socket`|`dict`|no||
`spec . template . spec . containers . lifecycle . post_start . tcp_socket . host`|`str`|no||
`spec . template . spec . containers . lifecycle . post_start . tcp_socket . port`||no||
`spec . template . spec . containers . lifecycle . pre_stop`|`dict`|no||
`spec . template . spec . containers . lifecycle . pre_stop . exec`|`dict`|no||
`spec . template . spec . containers . lifecycle . pre_stop . exec . command`|`list` (of `str`)|no||
`spec . template . spec . containers . lifecycle . pre_stop . http_get`|`dict`|no||
`spec . template . spec . containers . lifecycle . pre_stop . http_get . host`|`str`|no||
`spec . template . spec . containers . lifecycle . pre_stop . http_get . http_headers`|`list` (of `dict`)|no||
`spec . template . spec . containers . lifecycle . pre_stop . http_get . http_headers . name`|`str`|no||
`spec . template . spec . containers . lifecycle . pre_stop . http_get . http_headers . value`|`str`|no||
`spec . template . spec . containers . lifecycle . pre_stop . http_get . path`|`str`|no||
`spec . template . spec . containers . lifecycle . pre_stop . http_get . port`||no||
`spec . template . spec . containers . lifecycle . pre_stop . http_get . scheme`|`str`|no||
`spec . template . spec . containers . lifecycle . pre_stop . tcp_socket`|`dict`|no||
`spec . template . spec . containers . lifecycle . pre_stop . tcp_socket . host`|`str`|no||
`spec . template . spec . containers . lifecycle . pre_stop . tcp_socket . port`||no||
`spec . template . spec . containers . liveness_probe`|`dict`|no||
`spec . template . spec . containers . liveness_probe . exec`|`dict`|no||
`spec . template . spec . containers . liveness_probe . exec . command`|`list` (of `str`)|no||
`spec . template . spec . containers . liveness_probe . failure_threshold`|`int`|no||
`spec . template . spec . containers . liveness_probe . http_get`|`dict`|no||
`spec . template . spec . containers . liveness_probe . http_get . host`|`str`|no||
`spec . template . spec . containers . liveness_probe . http_get . http_headers`|`list` (of `dict`)|no||
`spec . template . spec . containers . liveness_probe . http_get . http_headers . name`|`str`|no||
`spec . template . spec . containers . liveness_probe . http_get . http_headers . value`|`str`|no||
`spec . template . spec . containers . liveness_probe . http_get . path`|`str`|no||
`spec . template . spec . containers . liveness_probe . http_get . port`||no||
`spec . template . spec . containers . liveness_probe . http_get . scheme`|`str`|no||
`spec . template . spec . containers . liveness_probe . initial_delay_seconds`|`int`|no||
`spec . template . spec . containers . liveness_probe . period_seconds`|`int`|no||
`spec . template . spec . containers . liveness_probe . success_threshold`|`int`|no||
`spec . template . spec . containers . liveness_probe . tcp_socket`|`dict`|no||
`spec . template . spec . containers . liveness_probe . tcp_socket . host`|`str`|no||
`spec . template . spec . containers . liveness_probe . tcp_socket . port`||no||
`spec . template . spec . containers . liveness_probe . timeout_seconds`|`int`|no||
`spec . template . spec . containers . name`|`str`|no||
`spec . template . spec . containers . ports`|`list` (of `dict`)|no||
`spec . template . spec . containers . ports . container_port`|`int`|no||
`spec . template . spec . containers . ports . host_IP`|`str`|no||
`spec . template . spec . containers . ports . host_port`|`int`|no||
`spec . template . spec . containers . ports . name`|`str`|no||
`spec . template . spec . containers . ports . protocol`|`str`|no||
`spec . template . spec . containers . readiness_probe`|`dict`|no||
`spec . template . spec . containers . readiness_probe . exec`|`dict`|no||
`spec . template . spec . containers . readiness_probe . exec . command`|`list` (of `str`)|no||
`spec . template . spec . containers . readiness_probe . failure_threshold`|`int`|no||
`spec . template . spec . containers . readiness_probe . http_get`|`dict`|no||
`spec . template . spec . containers . readiness_probe . http_get . host`|`str`|no||
`spec . template . spec . containers . readiness_probe . http_get . http_headers`|`list` (of `dict`)|no||
`spec . template . spec . containers . readiness_probe . http_get . http_headers . name`|`str`|no||
`spec . template . spec . containers . readiness_probe . http_get . http_headers . value`|`str`|no||
`spec . template . spec . containers . readiness_probe . http_get . path`|`str`|no||
`spec . template . spec . containers . readiness_probe . http_get . port`||no||
`spec . template . spec . containers . readiness_probe . http_get . scheme`|`str`|no||
`spec . template . spec . containers . readiness_probe . initial_delay_seconds`|`int`|no||
`spec . template . spec . containers . readiness_probe . period_seconds`|`int`|no||
`spec . template . spec . containers . readiness_probe . success_threshold`|`int`|no||
`spec . template . spec . containers . readiness_probe . tcp_socket`|`dict`|no||
`spec . template . spec . containers . readiness_probe . tcp_socket . host`|`str`|no||
`spec . template . spec . containers . readiness_probe . tcp_socket . port`||no||
`spec . template . spec . containers . readiness_probe . timeout_seconds`|`int`|no||
`spec . template . spec . containers . resources`|`dict`|no||
`spec . template . spec . containers . resources . limits`|`dict`|no||
`spec . template . spec . containers . resources . requests`|`dict`|no||
`spec . template . spec . containers . security_context`|`dict`|no||
`spec . template . spec . containers . security_context . allow_privilege_escalation`|`bool`|no||
`spec . template . spec . containers . security_context . capabilities`|`dict`|no||
`spec . template . spec . containers . security_context . capabilities . add`|`list` (of `str`)|no||
`spec . template . spec . containers . security_context . capabilities . drop`|`list` (of `str`)|no||
`spec . template . spec . containers . security_context . privileged`|`bool`|no||
`spec . template . spec . containers . security_context . proc_mount`|`str`|no||
`spec . template . spec . containers . security_context . read_only_root_filesystem`|`bool`|no||
`spec . template . spec . containers . security_context . run_as_group`|`int`|no||
`spec . template . spec . containers . security_context . run_as_non_root`|`bool`|no||
`spec . template . spec . containers . security_context . run_as_user`|`int`|no||
`spec . template . spec . containers . security_context . selinux_options`|`dict`|no||
`spec . template . spec . containers . security_context . selinux_options . level`|`str`|no||
`spec . template . spec . containers . security_context . selinux_options . role`|`str`|no||
`spec . template . spec . containers . security_context . selinux_options . type`|`str`|no||
`spec . template . spec . containers . security_context . selinux_options . user`|`str`|no||
`spec . template . spec . containers . stdin`|`bool`|no||
`spec . template . spec . containers . stdin_once`|`bool`|no||
`spec . template . spec . containers . termination_message_path`|`str`|no||
`spec . template . spec . containers . termination_message_policy`|`str`|no||
`spec . template . spec . containers . tty`|`bool`|no||
`spec . template . spec . containers . volume_devices`|`list` (of `dict`)|no||
`spec . template . spec . containers . volume_devices . device_path`|`str`|no||
`spec . template . spec . containers . volume_devices . name`|`str`|no||
`spec . template . spec . containers . volume_mounts`|`list` (of `dict`)|no||
`spec . template . spec . containers . volume_mounts . mount_path`|`str`|no||
`spec . template . spec . containers . volume_mounts . mount_propagation`|`str`|no||
`spec . template . spec . containers . volume_mounts . name`|`str`|no||
`spec . template . spec . containers . volume_mounts . read_only`|`bool`|no||
`spec . template . spec . containers . volume_mounts . sub_path`|`str`|no||
`spec . template . spec . containers . volume_mounts . sub_path_expr`|`str`|no||
`spec . template . spec . containers . working_dir`|`str`|no||
`spec . template . spec . dns_config`|`dict`|no||
`spec . template . spec . dns_policy`|`str`|no||
`spec . template . spec . enable_service_links`|`bool`|no||
`spec . template . spec . host_IPC`|`bool`|no||
`spec . template . spec . host_PID`|`bool`|no||
`spec . template . spec . host_aliases`|`list` (of `dict`)|no||
`spec . template . spec . host_network`|`bool`|no||
`spec . template . spec . hostname`|`str`|no||
`spec . template . spec . image_pull_secrets`|`list` (of `dict`)|no||
`spec . template . spec . init_containers`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . args`|`list` (of `str`)|no||
`spec . template . spec . init_containers . command`|`list` (of `str`)|no||
`spec . template . spec . init_containers . env`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . env . name`|`str`|yes||
`spec . template . spec . init_containers . env . value`|`str`|no||
`spec . template . spec . init_containers . env . value_from`|`dict`|no||
`spec . template . spec . init_containers . env . value_from . config_map_key_ref`|`dict`|no||
`spec . template . spec . init_containers . env . value_from . config_map_key_ref . key`|`str`|yes||
`spec . template . spec . init_containers . env . value_from . config_map_key_ref . name`|`str`|yes||
`spec . template . spec . init_containers . env . value_from . config_map_key_ref . optional`|`bool`|no||
`spec . template . spec . init_containers . env . value_from . field_ref`|`dict`|no||
`spec . template . spec . init_containers . env . value_from . field_ref . api_version`|`str`|no||
`spec . template . spec . init_containers . env . value_from . field_ref . field_path`|`str`|yes||
`spec . template . spec . init_containers . env . value_from . resource_field_ref`|`dict`|no||
`spec . template . spec . init_containers . env . value_from . resource_field_ref . container_name`|`str`|no||
`spec . template . spec . init_containers . env . value_from . resource_field_ref . divisor`||no||
`spec . template . spec . init_containers . env . value_from . resource_field_ref . resource`|`str`|yes||
`spec . template . spec . init_containers . env . value_from . secret_key_ref`|`dict`|no||
`spec . template . spec . init_containers . env . value_from . secret_key_ref . key`|`str`|yes||
`spec . template . spec . init_containers . env . value_from . secret_key_ref . name`|`str`|yes||
`spec . template . spec . init_containers . env . value_from . secret_key_ref . optional`|`bool`|no||
`spec . template . spec . init_containers . env_from`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . image`|`str`|no||
`spec . template . spec . init_containers . image_pull_policy`|`str`|no||
`spec . template . spec . init_containers . lifecycle`|`dict`|no||
`spec . template . spec . init_containers . lifecycle . post_start`|`dict`|no||
`spec . template . spec . init_containers . lifecycle . post_start . exec`|`dict`|no||
`spec . template . spec . init_containers . lifecycle . post_start . exec . command`|`list` (of `str`)|no||
`spec . template . spec . init_containers . lifecycle . post_start . http_get`|`dict`|no||
`spec . template . spec . init_containers . lifecycle . post_start . http_get . host`|`str`|no||
`spec . template . spec . init_containers . lifecycle . post_start . http_get . http_headers`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . lifecycle . post_start . http_get . http_headers . name`|`str`|no||
`spec . template . spec . init_containers . lifecycle . post_start . http_get . http_headers . value`|`str`|no||
`spec . template . spec . init_containers . lifecycle . post_start . http_get . path`|`str`|no||
`spec . template . spec . init_containers . lifecycle . post_start . http_get . port`||no||
`spec . template . spec . init_containers . lifecycle . post_start . http_get . scheme`|`str`|no||
`spec . template . spec . init_containers . lifecycle . post_start . tcp_socket`|`dict`|no||
`spec . template . spec . init_containers . lifecycle . post_start . tcp_socket . host`|`str`|no||
`spec . template . spec . init_containers . lifecycle . post_start . tcp_socket . port`||no||
`spec . template . spec . init_containers . lifecycle . pre_stop`|`dict`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . exec`|`dict`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . exec . command`|`list` (of `str`)|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . http_get`|`dict`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . http_get . host`|`str`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . http_get . http_headers`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . http_get . http_headers . name`|`str`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . http_get . http_headers . value`|`str`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . http_get . path`|`str`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . http_get . port`||no||
`spec . template . spec . init_containers . lifecycle . pre_stop . http_get . scheme`|`str`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . tcp_socket`|`dict`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . tcp_socket . host`|`str`|no||
`spec . template . spec . init_containers . lifecycle . pre_stop . tcp_socket . port`||no||
`spec . template . spec . init_containers . liveness_probe`|`dict`|no||
`spec . template . spec . init_containers . liveness_probe . exec`|`dict`|no||
`spec . template . spec . init_containers . liveness_probe . exec . command`|`list` (of `str`)|no||
`spec . template . spec . init_containers . liveness_probe . failure_threshold`|`int`|no||
`spec . template . spec . init_containers . liveness_probe . http_get`|`dict`|no||
`spec . template . spec . init_containers . liveness_probe . http_get . host`|`str`|no||
`spec . template . spec . init_containers . liveness_probe . http_get . http_headers`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . liveness_probe . http_get . http_headers . name`|`str`|no||
`spec . template . spec . init_containers . liveness_probe . http_get . http_headers . value`|`str`|no||
`spec . template . spec . init_containers . liveness_probe . http_get . path`|`str`|no||
`spec . template . spec . init_containers . liveness_probe . http_get . port`||no||
`spec . template . spec . init_containers . liveness_probe . http_get . scheme`|`str`|no||
`spec . template . spec . init_containers . liveness_probe . initial_delay_seconds`|`int`|no||
`spec . template . spec . init_containers . liveness_probe . period_seconds`|`int`|no||
`spec . template . spec . init_containers . liveness_probe . success_threshold`|`int`|no||
`spec . template . spec . init_containers . liveness_probe . tcp_socket`|`dict`|no||
`spec . template . spec . init_containers . liveness_probe . tcp_socket . host`|`str`|no||
`spec . template . spec . init_containers . liveness_probe . tcp_socket . port`||no||
`spec . template . spec . init_containers . liveness_probe . timeout_seconds`|`int`|no||
`spec . template . spec . init_containers . name`|`str`|no||
`spec . template . spec . init_containers . ports`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . ports . container_port`|`int`|no||
`spec . template . spec . init_containers . ports . host_IP`|`str`|no||
`spec . template . spec . init_containers . ports . host_port`|`int`|no||
`spec . template . spec . init_containers . ports . name`|`str`|no||
`spec . template . spec . init_containers . ports . protocol`|`str`|no||
`spec . template . spec . init_containers . readiness_probe`|`dict`|no||
`spec . template . spec . init_containers . readiness_probe . exec`|`dict`|no||
`spec . template . spec . init_containers . readiness_probe . exec . command`|`list` (of `str`)|no||
`spec . template . spec . init_containers . readiness_probe . failure_threshold`|`int`|no||
`spec . template . spec . init_containers . readiness_probe . http_get`|`dict`|no||
`spec . template . spec . init_containers . readiness_probe . http_get . host`|`str`|no||
`spec . template . spec . init_containers . readiness_probe . http_get . http_headers`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . readiness_probe . http_get . http_headers . name`|`str`|no||
`spec . template . spec . init_containers . readiness_probe . http_get . http_headers . value`|`str`|no||
`spec . template . spec . init_containers . readiness_probe . http_get . path`|`str`|no||
`spec . template . spec . init_containers . readiness_probe . http_get . port`||no||
`spec . template . spec . init_containers . readiness_probe . http_get . scheme`|`str`|no||
`spec . template . spec . init_containers . readiness_probe . initial_delay_seconds`|`int`|no||
`spec . template . spec . init_containers . readiness_probe . period_seconds`|`int`|no||
`spec . template . spec . init_containers . readiness_probe . success_threshold`|`int`|no||
`spec . template . spec . init_containers . readiness_probe . tcp_socket`|`dict`|no||
`spec . template . spec . init_containers . readiness_probe . tcp_socket . host`|`str`|no||
`spec . template . spec . init_containers . readiness_probe . tcp_socket . port`||no||
`spec . template . spec . init_containers . readiness_probe . timeout_seconds`|`int`|no||
`spec . template . spec . init_containers . resources`|`dict`|no||
`spec . template . spec . init_containers . resources . limits`|`dict`|no||
`spec . template . spec . init_containers . resources . requests`|`dict`|no||
`spec . template . spec . init_containers . security_context`|`dict`|no||
`spec . template . spec . init_containers . security_context . allow_privilege_escalation`|`bool`|no||
`spec . template . spec . init_containers . security_context . capabilities`|`dict`|no||
`spec . template . spec . init_containers . security_context . capabilities . add`|`list` (of `str`)|no||
`spec . template . spec . init_containers . security_context . capabilities . drop`|`list` (of `str`)|no||
`spec . template . spec . init_containers . security_context . privileged`|`bool`|no||
`spec . template . spec . init_containers . security_context . proc_mount`|`str`|no||
`spec . template . spec . init_containers . security_context . read_only_root_filesystem`|`bool`|no||
`spec . template . spec . init_containers . security_context . run_as_group`|`int`|no||
`spec . template . spec . init_containers . security_context . run_as_non_root`|`bool`|no||
`spec . template . spec . init_containers . security_context . run_as_user`|`int`|no||
`spec . template . spec . init_containers . security_context . selinux_options`|`dict`|no||
`spec . template . spec . init_containers . security_context . selinux_options . level`|`str`|no||
`spec . template . spec . init_containers . security_context . selinux_options . role`|`str`|no||
`spec . template . spec . init_containers . security_context . selinux_options . type`|`str`|no||
`spec . template . spec . init_containers . security_context . selinux_options . user`|`str`|no||
`spec . template . spec . init_containers . stdin`|`bool`|no||
`spec . template . spec . init_containers . stdin_once`|`bool`|no||
`spec . template . spec . init_containers . termination_message_path`|`str`|no||
`spec . template . spec . init_containers . termination_message_policy`|`str`|no||
`spec . template . spec . init_containers . tty`|`bool`|no||
`spec . template . spec . init_containers . volume_devices`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . volume_devices . device_path`|`str`|no||
`spec . template . spec . init_containers . volume_devices . name`|`str`|no||
`spec . template . spec . init_containers . volume_mounts`|`list` (of `dict`)|no||
`spec . template . spec . init_containers . volume_mounts . mount_path`|`str`|no||
`spec . template . spec . init_containers . volume_mounts . mount_propagation`|`str`|no||
`spec . template . spec . init_containers . volume_mounts . name`|`str`|no||
`spec . template . spec . init_containers . volume_mounts . read_only`|`bool`|no||
`spec . template . spec . init_containers . volume_mounts . sub_path`|`str`|no||
`spec . template . spec . init_containers . volume_mounts . sub_path_expr`|`str`|no||
`spec . template . spec . init_containers . working_dir`|`str`|no||
`spec . template . spec . node_name`|`str`|no||
`spec . template . spec . node_selector`|`dict`|no||
`spec . template . spec . priority`|`int`|no||
`spec . template . spec . priority_class_name`|`str`|no||
`spec . template . spec . restart_policy`|`str`|no||
`spec . template . spec . scheduler_name`|`str`|no||
`spec . template . spec . security_context`|`dict`|no||
`spec . template . spec . security_context . fs_group`|`int`|no||
`spec . template . spec . security_context . run_as_group`|`int`|no||
`spec . template . spec . security_context . run_as_non_root`|`bool`|no||
`spec . template . spec . security_context . run_as_user`|`int`|no||
`spec . template . spec . security_context . selinux_options`|`dict`|no||
`spec . template . spec . security_context . selinux_options . level`|`str`|no||
`spec . template . spec . security_context . selinux_options . role`|`str`|no||
`spec . template . spec . security_context . selinux_options . type`|`str`|no||
`spec . template . spec . security_context . selinux_options . user`|`str`|no||
`spec . template . spec . security_context . supplemental_groups`|`list` (of `int`)|no||
`spec . template . spec . security_context . sysctls`|`list` (of `dict`)|no||
`spec . template . spec . security_context . sysctls . name`|`str`|no||
`spec . template . spec . security_context . sysctls . value`|`str`|no||
`spec . template . spec . service_account_name`|`str`|no||
`spec . template . spec . share_process_namespace`|`bool`|no||
`spec . template . spec . subdomain`|`str`|no||
`spec . template . spec . termination_grace_period_seconds`|`int`|no||
`spec . template . spec . tolerations`|`list` (of `dict`)|no||
`spec . template . spec . volumes`|`list` (of `dict`)|no||
`spec . update_strategy`|`dict`|no||
`spec . update_strategy . rolling_update`|`dict`|no||
`spec . update_strategy . rolling_update . partition`|`int`|no||
`spec . update_strategy . type`|`str`|no||
`spec . volume_claim_templates`|`list` (of `dict`)|no||
`spec . volume_claim_templates . metadata`|`dict`|yes||
`spec . volume_claim_templates . metadata . annotations`|`dict`|no||
`spec . volume_claim_templates . metadata . labels`|`dict`|no||
`spec . volume_claim_templates . metadata . name`|`str`|no||
`spec . volume_claim_templates . metadata . namespace`|`str`|no||
`spec . volume_claim_templates . spec`|`dict`|yes||
`spec . volume_claim_templates . spec . access_modes`|`list` (of `str`)|no||
`spec . volume_claim_templates . spec . data_source`|`dict`|no||
`spec . volume_claim_templates . spec . data_source . api_group`|`str`|no||
`spec . volume_claim_templates . spec . data_source . kind`|`str`|no||
`spec . volume_claim_templates . spec . data_source . name`|`str`|no||
`spec . volume_claim_templates . spec . resources`|`dict`|no||
`spec . volume_claim_templates . spec . resources . limits`|`dict`|no||
`spec . volume_claim_templates . spec . resources . requests`|`dict`|no||
`spec . volume_claim_templates . spec . selector`|`dict`|no||
`spec . volume_claim_templates . spec . selector . match_expressions`|`list` (of `dict`)|no||
`spec . volume_claim_templates . spec . selector . match_expressions . key`|`str`|yes||
`spec . volume_claim_templates . spec . selector . match_expressions . operator`|`str`|yes||
`spec . volume_claim_templates . spec . selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . volume_claim_templates . spec . selector . match_labels`|`dict`|no||
`spec . volume_claim_templates . spec . storage_class_name`|`str`|no||
`spec . volume_claim_templates . spec . volume_mode`|`str`|no||
`spec . volume_claim_templates . spec . volume_name`|`str`|no||


