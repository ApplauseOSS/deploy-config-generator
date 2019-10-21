<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_cronjob

Kubernetes cronjob output plugin

### Parameters


#### Deploy config section: kube_cronjobs

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|yes||
`metadata . namespace`|`str`|no||
`spec`|`dict`|yes||
`spec . concurrency_policy`|`str`|no||
`spec . failed_jobs_history_limit`|`int`|no||
`spec . job_template`|`dict`|yes||
`spec . job_template . metadata`|`dict`|no||
`spec . job_template . metadata . annotations`|`dict`|no||
`spec . job_template . metadata . labels`|`dict`|no||
`spec . job_template . metadata . name`|`str`|yes||
`spec . job_template . metadata . namespace`|`str`|no||
`spec . job_template . spec`|`dict`|yes||
`spec . job_template . spec . active_deadline_seconds`|`int`|no||
`spec . job_template . spec . backoff_limit`|`int`|no||
`spec . job_template . spec . completions`|`int`|no||
`spec . job_template . spec . manual_selector`|`bool`|no||
`spec . job_template . spec . parallelism`|`int`|no||
`spec . job_template . spec . selector`|`dict`|no||
`spec . job_template . spec . selector . match_expressions`|`list` (of `dict`)|no||
`spec . job_template . spec . selector . match_expressions . key`|`str`|yes||
`spec . job_template . spec . selector . match_expressions . operator`|`str`|yes||
`spec . job_template . spec . selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . job_template . spec . selector . match_labels`|`dict`|no||
`spec . job_template . spec . template`|`dict`|yes||
`spec . job_template . spec . template . metadata`|`dict`|yes||
`spec . job_template . spec . template . metadata . annotations`|`dict`|no||
`spec . job_template . spec . template . metadata . labels`|`dict`|no||
`spec . job_template . spec . template . metadata . name`|`str`|yes||
`spec . job_template . spec . template . metadata . namespace`|`str`|no||
`spec . job_template . spec . template . spec`|`dict`|yes||
`spec . job_template . spec . template . spec . active_deadline_seconds`|`int`|no||
`spec . job_template . spec . template . spec . affinity`|`dict`|no||
`spec . job_template . spec . template . spec . automount_service_account_token`|`bool`|no||
`spec . job_template . spec . template . spec . containers`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . containers . args`|`list` (of `str`)|no||
`spec . job_template . spec . template . spec . containers . command`|`list` (of `str`)|no||
`spec . job_template . spec . template . spec . containers . env`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . containers . env . name`|`str`|yes||
`spec . job_template . spec . template . spec . containers . env . value`|`str`|no||
`spec . job_template . spec . template . spec . containers . env . value_from`|`dict`|no||
`spec . job_template . spec . template . spec . containers . env_from`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . containers . image`|`str`|no||
`spec . job_template . spec . template . spec . containers . image_pull_policy`|`str`|no||
`spec . job_template . spec . template . spec . containers . lifecycle`|`dict`|no||
`spec . job_template . spec . template . spec . containers . liveness_probe`|`dict`|no||
`spec . job_template . spec . template . spec . containers . name`|`str`|no||
`spec . job_template . spec . template . spec . containers . ports`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . containers . ports . container_port`|`int`|no||
`spec . job_template . spec . template . spec . containers . ports . host_IP`|`str`|no||
`spec . job_template . spec . template . spec . containers . ports . host_port`|`int`|no||
`spec . job_template . spec . template . spec . containers . ports . name`|`str`|no||
`spec . job_template . spec . template . spec . containers . ports . protocol`|`str`|no||
`spec . job_template . spec . template . spec . containers . readiness_probe`|`dict`|no||
`spec . job_template . spec . template . spec . containers . resources`|`dict`|no||
`spec . job_template . spec . template . spec . containers . security_context`|`dict`|no||
`spec . job_template . spec . template . spec . containers . stdin`|`bool`|no||
`spec . job_template . spec . template . spec . containers . stdin_once`|`bool`|no||
`spec . job_template . spec . template . spec . containers . termination_message_path`|`str`|no||
`spec . job_template . spec . template . spec . containers . termination_message_policy`|`str`|no||
`spec . job_template . spec . template . spec . containers . tty`|`bool`|no||
`spec . job_template . spec . template . spec . containers . volume_devices`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . containers . volume_mounts`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . containers . working_dir`|`str`|no||
`spec . job_template . spec . template . spec . dns_config`|`dict`|no||
`spec . job_template . spec . template . spec . dns_policy`|`str`|no||
`spec . job_template . spec . template . spec . host_IPC`|`bool`|no||
`spec . job_template . spec . template . spec . host_PID`|`bool`|no||
`spec . job_template . spec . template . spec . host_aliases`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . host_network`|`bool`|no||
`spec . job_template . spec . template . spec . hostname`|`str`|no||
`spec . job_template . spec . template . spec . image_pull_secrets`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . init_containers`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . init_containers . args`|`list` (of `str`)|no||
`spec . job_template . spec . template . spec . init_containers . command`|`list` (of `str`)|no||
`spec . job_template . spec . template . spec . init_containers . env`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . init_containers . env . name`|`str`|yes||
`spec . job_template . spec . template . spec . init_containers . env . value`|`str`|no||
`spec . job_template . spec . template . spec . init_containers . env . value_from`|`dict`|no||
`spec . job_template . spec . template . spec . init_containers . env_from`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . init_containers . image`|`str`|no||
`spec . job_template . spec . template . spec . init_containers . image_pull_policy`|`str`|no||
`spec . job_template . spec . template . spec . init_containers . lifecycle`|`dict`|no||
`spec . job_template . spec . template . spec . init_containers . liveness_probe`|`dict`|no||
`spec . job_template . spec . template . spec . init_containers . name`|`str`|no||
`spec . job_template . spec . template . spec . init_containers . ports`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . init_containers . ports . container_port`|`int`|no||
`spec . job_template . spec . template . spec . init_containers . ports . host_IP`|`str`|no||
`spec . job_template . spec . template . spec . init_containers . ports . host_port`|`int`|no||
`spec . job_template . spec . template . spec . init_containers . ports . name`|`str`|no||
`spec . job_template . spec . template . spec . init_containers . ports . protocol`|`str`|no||
`spec . job_template . spec . template . spec . init_containers . readiness_probe`|`dict`|no||
`spec . job_template . spec . template . spec . init_containers . resources`|`dict`|no||
`spec . job_template . spec . template . spec . init_containers . security_context`|`dict`|no||
`spec . job_template . spec . template . spec . init_containers . stdin`|`bool`|no||
`spec . job_template . spec . template . spec . init_containers . stdin_once`|`bool`|no||
`spec . job_template . spec . template . spec . init_containers . termination_message_path`|`str`|no||
`spec . job_template . spec . template . spec . init_containers . termination_message_policy`|`str`|no||
`spec . job_template . spec . template . spec . init_containers . tty`|`bool`|no||
`spec . job_template . spec . template . spec . init_containers . volume_devices`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . init_containers . volume_mounts`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . init_containers . working_dir`|`str`|no||
`spec . job_template . spec . template . spec . node_name`|`str`|no||
`spec . job_template . spec . template . spec . node_selector`|`dict`|no||
`spec . job_template . spec . template . spec . priority`|`int`|no||
`spec . job_template . spec . template . spec . priority_class_name`|`str`|no||
`spec . job_template . spec . template . spec . restart_policy`|`str`|no||
`spec . job_template . spec . template . spec . scheduler_name`|`str`|no||
`spec . job_template . spec . template . spec . security_context`|`dict`|no||
`spec . job_template . spec . template . spec . service_account_name`|`str`|no||
`spec . job_template . spec . template . spec . share_process_namespace`|`bool`|no||
`spec . job_template . spec . template . spec . subdomain`|`str`|no||
`spec . job_template . spec . template . spec . termination_grace_period_seconds`|`int`|no||
`spec . job_template . spec . template . spec . tolerations`|`list` (of `dict`)|no||
`spec . job_template . spec . template . spec . volumes`|`list` (of `dict`)|no||
`spec . job_template . spec . ttl_seconds_after_finished`|`int`|no||
`spec . schedule`|`str`|yes||
`spec . starting_deadline_seconds`|`int`|no||
`spec . successful_jobs_history_limit`|`int`|no||
`spec . suspend`|`bool`|no||

