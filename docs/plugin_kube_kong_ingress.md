<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_kong_ingress

Kubernetes KongIngress output plugin

### Parameters


#### Deploy config section: kong_ingresses

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`proxy`|`dict`|no||
`proxy . connect_timeout`|`int`|no||
`proxy . path`|`str`|no||
`proxy . protocol`|`str`|no||
`proxy . read_timeout`|`int`|no||
`proxy . retries`|`int`|no||
`proxy . write_timeout`|`int`|no||
`route`|`dict`|no||
`route . https_redirect_status_code`|`int`|no||
`route . methods`|`list` (of `str`)|no||
`route . path_handling`|`str`|no||
`route . preserve_host`|`bool`|no||
`route . protocols`|`list` (of `str`)|no||
`route . regex_priority`|`int`|no||
`route . strip_path`|`bool`|no||
`upstream`|`dict`|no||
`upstream . hash_fallback`|`str`|no||
`upstream . hash_on`|`str`|no||
`upstream . healthchecks`|`dict`|no||
`upstream . healthchecks . active`|`dict`|no||
`upstream . healthchecks . active . concurrency`|`int`|no||
`upstream . healthchecks . active . healthy`|`dict`|no||
`upstream . healthchecks . active . healthy . http_statuses`|`list` (of `int`)|no||
`upstream . healthchecks . active . healthy . interval`|`int`|no||
`upstream . healthchecks . active . healthy . successes`|`int`|no||
`upstream . healthchecks . active . http_path`|`str`|no||
`upstream . healthchecks . active . timeout`|`int`|no||
`upstream . healthchecks . active . unhealthy`|`dict`|no||
`upstream . healthchecks . active . unhealthy . http_failures`|`int`|no||
`upstream . healthchecks . active . unhealthy . http_statuses`|`list` (of `int`)|no||
`upstream . healthchecks . active . unhealthy . interval`|`int`|no||
`upstream . healthchecks . active . unhealthy . tcp_failures`|`int`|no||
`upstream . healthchecks . active . unhealthy . timeouts`|`int`|no||
`upstream . healthchecks . passive`|`dict`|no||
`upstream . healthchecks . passive . healthy`|`dict`|no||
`upstream . healthchecks . passive . healthy . http_statuses`|`list` (of `int`)|no||
`upstream . healthchecks . passive . healthy . successes`|`int`|no||
`upstream . healthchecks . passive . unhealthy`|`dict`|no||
`upstream . healthchecks . passive . unhealthy . http_failures`|`int`|no||
`upstream . healthchecks . passive . unhealthy . http_statuses`|`list` (of `int`)|no||
`upstream . healthchecks . passive . unhealthy . tcp_failures`|`int`|no||
`upstream . healthchecks . passive . unhealthy . timeouts`|`int`|no||
`upstream . slots`|`int`|no||


