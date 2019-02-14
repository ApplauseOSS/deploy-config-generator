<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# metronome

Metronome output plugin

### Parameters


#### Deploy config section: jobs

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`artifacts`||no||
`cmd`||yes||
`cpus`||yes||
`description`||no||
`disk`||yes||
`docker_image`||no||
`env`|`dict`|no||
`id`||yes||
`labels`||no||
`max_launch_delay`||no||
`mem`||yes||
`restart`|`dict`|no||
`restart . active_deadline_seconds`|`int`|no||
`restart . policy`||yes||
`schedules`||no||
`secrets`|`list` (of `dict`)|no||List of secrets from the DC/OS secret store
`secrets . name`||yes||Name of secret to expose for env/volumes
`secrets . source`||yes||Name of secret in DC/OS secret store
`user`||no||
`volumes`||no||


