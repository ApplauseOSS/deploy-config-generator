<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_secret

Kubernetes secret output plugin

### Parameters


#### Deploy config section: kube_secrets

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`data`|`dict`|no||Values will be automatically base64-encoded as expected by the Kubernetes API
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|yes||
`metadata . namespace`|`str`|no||
`string_data`|`dict`|no||
`type`|`str`|yes||


