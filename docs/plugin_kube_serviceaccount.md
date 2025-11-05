<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_serviceaccount

Kubernetes service account output plugin

### Parameters


#### Deploy config section: kube_serviceaccounts

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`automount_service_account_token`|`bool`|no||
`image_pull_secrets`|`list` (of `dict`)|no||
`image_pull_secrets . name`|`str`|no||
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`secrets`|`list` (of `dict`)|no||
`secrets . name`|`str`|no||


