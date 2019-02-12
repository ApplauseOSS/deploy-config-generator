<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# marathon

Marathon output plugin

### Parameters


#### Deploy config section: apps

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`accepted_resource_roles`|`list`|no||
`args`|`list`|no||Arguments to pass to container
`cmd`||no||Command to execute (optional)
`constraints`|`list`|no||
`container_labels`|`list`|no||
`cpus`|`float`|yes||
`disk`|`int`|yes||
`docker_network`||no|`BRIDGE`|
`docker_privileged`|`bool`|no|`False`|
`env`|`dict`|no||Environment variables to pass to the container
`fetch`|`list` (of `dict`)|no||
`fetch . cache`|`bool`|no||
`fetch . condition`||no||Condition to evaluate before applying fetch config. The vars `fetch` (current fetch definition) and `fetch_index` (index of current fetch defintion in list) are available
`fetch . executable`|`bool`|no||
`fetch . extract`|`bool`|no||
`fetch . uri`|`str`|no||
`health_checks`|`list` (of `dict`)|no||
`health_checks . command`|`str`|no||
`health_checks . delay_seconds`|`int`|no||
`health_checks . grace_period_seconds`|`int`|no||
`health_checks . interval_seconds`|`int`|no||
`health_checks . max_consecutive_failures`|`int`|no||
`health_checks . path`|`str`|no||
`health_checks . port`|`int`|no||
`health_checks . port_index`|`int`|no||
`health_checks . protocol`||no|`MESOS_HTTP`|
`health_checks . timeout_seconds`|`int`|no||
`id`||yes||Unique ID for app in Marathon
`image`||yes||Docker image to use
`instances`|`int`|no|`1`|
`labels`|`dict`|no||
`mem`|`float`|yes||
`port_definitions`|`list` (of `dict`)|no||List of port definitions (for HOST networking mode)
`port_definitions . labels`|`list` (of `dict`)|no||List of label name/value pairs to apply to port
`port_definitions . labels . condition`||no||Condition to evaluate before applying label. The vars `port` (current port definition) and `port_index` (index of current port definition in list) are available
`port_definitions . labels . name`||no||
`port_definitions . labels . value`||no||
`port_definitions . name`|`str`|no||
`port_definitions . port`|`int`|yes||
`port_definitions . protocol`|`str`|no||
`ports`|`list` (of `dict`)|no||List of port definitions
`ports . container_port`|`int`|yes||Port that the service is listening on inside the container
`ports . host_port`|`int`|no|`0`|
`ports . labels`|`list` (of `dict`)|no||List of label name/value pairs to apply to port
`ports . labels . condition`||no||Condition to evaluate before applying label. The vars `port` (current port definition) and `port_index` (index of current port definition in list) are available
`ports . labels . name`||no||
`ports . labels . value`||no||
`ports . protocol`|`str`|no|`tcp`|
`ports . service_port`|`int`|no|`0`|
`require_ports`|`bool`|no||Whether to require that ports specified in `port_definitions` are available (for HOST networking mode)
`secrets`|`list` (of `dict`)|no||List of secrets from the DC/OS secret store
`secrets . name`||yes||Name of secret to expose for env/volumes
`secrets . source`||yes||Name of secret in DC/OS secret store
`unreachable_strategy`|`dict`|no||
`unreachable_strategy . expunge_after_seconds`|`int`|no||
`unreachable_strategy . inactive_after_seconds`|`int`|no||
`upgrade_strategy`|`dict`|no||
`upgrade_strategy . maximum_over_capacity`|`float`|no||
`upgrade_strategy . minimum_health_capacity`|`float`|no||
`volumes`|`list` (of `dict`)|no||
`volumes . container_path`|`str`|no||
`volumes . host_path`|`str`|no||
`volumes . mode`|`str`|no||
`volumes . persistent`|`dict`|no||
`volumes . persistent . constraints`|`list`|no||
`volumes . persistent . max_size`|`float`|no||
`volumes . persistent . profile_name`|`str`|no||
`volumes . persistent . size`|`float`|no||
`volumes . persistent . type`|`str`|no||


