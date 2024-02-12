<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_pv

Kubernetes PersistentVolume output plugin

### Parameters


#### Deploy config section: kube_pvs

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`spec`|`dict`|yes||
`spec . access_modes`|`list` (of `str`)|yes||
`spec . capacity`|`dict`|yes||
`spec . capacity . storage`|`str`|no||
`spec . claim_ref`|`dict`|no||
`spec . claim_ref . api_version`|`str`|no||
`spec . claim_ref . kind`|`str`|no||
`spec . claim_ref . name`|`str`|no||
`spec . claim_ref . namespace`|`str`|no||
`spec . csi`|`dict`|no||
`spec . csi . driver`|`str`|no||
`spec . csi . fs_type`|`str`|no||
`spec . csi . read_only`|`bool`|no||
`spec . csi . volume_attributes`|`dict` (of `str`)|no||
`spec . csi . volume_handle`|`str`|no||
`spec . mount_options`|`list` (of `str`)|no||
`spec . nfs`|`dict`|no||
`spec . nfs . path`|`str`|yes||
`spec . nfs . server`|`str`|yes||
`spec . node_affinity`|`dict`|no||
`spec . node_affinity . required`|`dict`|no||
`spec . node_affinity . required . node_selector_terms`|`list` (of `dict`)|no||
`spec . persistent_volume_reclaim_policy`|`str`|no||
`spec . storage_class_name`|`str`|no||
`spec . volume_mode`|`str`|no||


