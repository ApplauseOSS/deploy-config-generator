<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_service

Kubernetes service output plugin

### Parameters


#### Deploy config section: kube_services

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`spec`|`dict`|yes||
`spec . cluster_IP`|`str`|no||
`spec . external_IPs`|`list` (of `str`)|no||
`spec . external_name`|`str`|no||
`spec . external_traffic_policy`|`str`|no||
`spec . health_check_node_port`|`int`|no||
`spec . load_balancer_IP`|`str`|no||
`spec . load_balancer_source_ranges`|`list` (of `str`)|no||
`spec . ports`|`list` (of `dict`)|no||
`spec . ports . name`|`str`|no||
`spec . ports . node_port`|`int`|no||
`spec . ports . port`|`int`|no||
`spec . ports . protocol`|`str`|no||
`spec . ports . target_port`||no||
`spec . publish_not_ready_addresses`|`bool`|no||
`spec . selector`|`dict`|no||
`spec . session_affinity`|`str`|no||
`spec . session_affinity_config`|`dict`|no||
`spec . session_affinity_config . client_IP`|`dict`|no||
`spec . session_affinity_config . client_IP . timeout_seconds`|`int`|no||
`spec . type`|`str`|no||


