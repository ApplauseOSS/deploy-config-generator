<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# marathon

Marathon output plugin

### Parameters


#### Deploy config section: apps

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`constraints`|`list`|no||
`container_labels`|`list`|no||
`cpus`||yes||
`disk`||yes||
`env`|`dict`|no||Environment variables to pass to the container
`fetch`|`list` (of `dict`)|no||
`health_checks`|`list` (of `dict`)|no||
`health_checks . command`|`str`|no||
`health_checks . delay_seconds`|`int`|no||
`health_checks . grace_period_seconds`|`int`|no||
`health_checks . interval_seconds`|`int`|no||
`health_checks . max_consecutive_failures`|`int`|no||
`health_checks . path`|`str`|no||
`health_checks . port_index`|`int`|no||
`health_checks . protocol`||no|`MESOS_HTTP`|
`health_checks . timeout_seconds`|`int`|no||
`id`||yes||Unique ID for app in Marathon
`image`||yes||Docker image to use
`instances`||no|`1`|
`labels`|`list`|no||
`mem`||yes||
`ports`|`list` (of `dict`)|no||List of port definitions
`ports . container_port`|`int`|yes||Port that the service is listening on inside the container
`ports . host_port`|`int`|no|`0`|
`ports . labels`|`list` (of `dict`)|no||List of label name/value pairs to apply to port
`ports . labels . condition`||no||Condition to evaluate before applying label. The vars `port` (current port definition) and `port_index` (index of current port defintion in list) are available
`ports . labels . name`||no||
`ports . labels . value`||no||
`ports . protocol`|`str`|no|`tcp`|
`ports . service_port`|`int`|no|`0`|
`unreachable_strategy`|`dict`|no||
`unreachable_strategy . expunge_after_seconds`|`int`|no||
`unreachable_strategy . inactive_after_seconds`|`int`|no||
`upgrade_strategy`|`dict`|no||
`upgrade_strategy . maximum_over_capacity`|`float`|no||
`upgrade_strategy . minimum_health_capacity`|`float`|no||

