<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_kong_plugin

Kubernetes KongPlugin output plugin

### Parameters


#### Deploy config section: kong_plugins

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`config`|`dict`|no||
`config_from`|`dict`|no||
`config_from . secret_key_ref`|`dict`|yes||
`config_from . secret_key_ref . key`|`str`|yes||
`config_from . secret_key_ref . name`|`str`|yes||
`disabled`|`bool`|no||
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`plugin`|`str`|no||


