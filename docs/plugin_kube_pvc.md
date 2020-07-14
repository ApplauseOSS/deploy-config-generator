<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_pvc

Kubernetes PersistentVolumeClaim output plugin

### Parameters


#### Deploy config section: kube_pvcs

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`spec`|`dict`|yes||
`spec . access_modes`|`list` (of `str`)|no||
`spec . data_source`|`dict`|no||
`spec . data_source . api_group`|`str`|no||
`spec . data_source . kind`|`str`|no||
`spec . data_source . name`|`str`|no||
`spec . resources`|`dict`|no||
`spec . resources . limits`|`dict`|no||
`spec . resources . requests`|`dict`|no||
`spec . selector`|`dict`|no||
`spec . selector . match_expressions`|`list` (of `dict`)|no||
`spec . selector . match_expressions . key`|`str`|yes||
`spec . selector . match_expressions . operator`|`str`|yes||
`spec . selector . match_expressions . values`|`list` (of `str`)|yes||
`spec . selector . match_labels`|`dict`|no||
`spec . storage_class_name`|`str`|yes||
`spec . volume_mode`|`str`|no||
`spec . volume_name`|`str`|no||


