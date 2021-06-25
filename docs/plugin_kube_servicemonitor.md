<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_servicemonitor

Kubernetes ServiceMonitor output plugin

### Parameters


#### Deploy config section: kube_servicemonitors

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`spec`|`dict`|yes||
`spec . endpoints`|`list` (of `dict`)|no||
`spec . endpoints . basic_auth`|`dict`|no||
`spec . endpoints . basic_auth . password`|`dict`|no||
`spec . endpoints . basic_auth . password . key`|`str`|yes||
`spec . endpoints . basic_auth . password . name`|`str`|no||
`spec . endpoints . basic_auth . password . optional`|`bool`|no||
`spec . endpoints . basic_auth . username`|`dict`|no||
`spec . endpoints . basic_auth . username . key`|`str`|yes||
`spec . endpoints . basic_auth . username . name`|`str`|no||
`spec . endpoints . basic_auth . username . optional`|`bool`|no||
`spec . endpoints . bearer_token_file`|`str`|no||
`spec . endpoints . bearer_token_secret`|`dict`|no||
`spec . endpoints . bearer_token_secret . key`|`str`|yes||
`spec . endpoints . bearer_token_secret . name`|`str`|no||
`spec . endpoints . bearer_token_secret . optional`|`bool`|no||
`spec . endpoints . honor_labels`|`bool`|no||
`spec . endpoints . honor_timestamps`|`bool`|no||
`spec . endpoints . interval`|`str`|no||
`spec . endpoints . metric_relabelings`|`list` (of `dict`)|no||
`spec . endpoints . metric_relabelings . action`|`str`|no||
`spec . endpoints . metric_relabelings . modulus`|`int`|no||
`spec . endpoints . metric_relabelings . regex`|`str`|no||
`spec . endpoints . metric_relabelings . replacement`|`str`|no||
`spec . endpoints . metric_relabelings . separator`|`str`|no||
`spec . endpoints . metric_relabelings . source_labels`|`list` (of `str`)|no||
`spec . endpoints . metric_relabelings . target_label`|`str`|no||
`spec . endpoints . params`|`dict`|no||
`spec . endpoints . params . additional_properties`|`list` (of `str`)|no||
`spec . endpoints . path`|`str`|no||
`spec . endpoints . port`|`str`|no||
`spec . endpoints . proxy_url`|`str`|no||
`spec . endpoints . relabelings`|`list` (of `dict`)|no||
`spec . endpoints . relabelings . action`|`str`|no||
`spec . endpoints . relabelings . modulus`|`int`|no||
`spec . endpoints . relabelings . regex`|`str`|no||
`spec . endpoints . relabelings . replacement`|`str`|no||
`spec . endpoints . relabelings . separator`|`str`|no||
`spec . endpoints . relabelings . source_labels`|`list` (of `str`)|no||
`spec . endpoints . relabelings . target_label`|`str`|no||
`spec . endpoints . scheme`|`str`|no||
`spec . endpoints . scrape_timeout`|`string`|no||
`spec . endpoints . target_port`||no||
`spec . endpoints . tls_config`|`dict`|no||
`spec . endpoints . tls_config . ca`|`dict`|no||
`spec . endpoints . tls_config . ca . config_map`|`dict`|no||
`spec . endpoints . tls_config . ca . config_map . key`|`str`|yes||
`spec . endpoints . tls_config . ca . config_map . name`|`str`|no||
`spec . endpoints . tls_config . ca . config_map . optional`|`bool`|no||
`spec . endpoints . tls_config . ca . secret`|`dict`|no||
`spec . endpoints . tls_config . ca . secret . key`|`str`|yes||
`spec . endpoints . tls_config . ca . secret . name`|`str`|no||
`spec . endpoints . tls_config . ca . secret . optional`|`bool`|no||
`spec . endpoints . tls_config . ca_file`|`str`|no||
`spec . endpoints . tls_config . cert`|`dict`|no||
`spec . endpoints . tls_config . cert . config_map`|`dict`|no||
`spec . endpoints . tls_config . cert . config_map . key`|`str`|yes||
`spec . endpoints . tls_config . cert . config_map . name`|`str`|no||
`spec . endpoints . tls_config . cert . config_map . optional`|`bool`|no||
`spec . endpoints . tls_config . cert . secret`|`dict`|no||
`spec . endpoints . tls_config . cert . secret . key`|`str`|yes||
`spec . endpoints . tls_config . cert . secret . name`|`str`|no||
`spec . endpoints . tls_config . cert . secret . optional`|`bool`|no||
`spec . endpoints . tls_config . cert_file`|`string`|no||
`spec . endpoints . tls_config . insecure_skip_verify`|`bool`|no||
`spec . endpoints . tls_config . keyFile`|`str`|no||
`spec . endpoints . tls_config . keySecret`|`dict`|no||
`spec . endpoints . tls_config . keySecret . key`|`str`|yes||
`spec . endpoints . tls_config . keySecret . name`|`str`|no||
`spec . endpoints . tls_config . keySecret . optional`|`bool`|no||
`spec . endpoints . tls_config . server_name`|`str`|no||
`spec . job_label`|`str`|no||
`spec . namespace_selector`|`dict`|no||
`spec . namespace_selector . any`|`bool`|no||
`spec . namespace_selector . match_names`|`list` (of `str`)|no||
`spec . pod_target_labels`|`list` (of `str`)|no||
`spec . sample_limit`|`int`|no||
`spec . selector`|`dict`|yes||
`spec . selector . match_expressions`|`list` (of `dict`)|no||
`spec . selector . match_expressions . key`|`str`|yes||
`spec . selector . match_expressions . operator`|`str`|yes||
`spec . selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . selector . match_labels`|`dict`|no||
`spec . targetLabels`|`list` (of `str`)|no||
`spec . targetLimit`|`int`|no||


