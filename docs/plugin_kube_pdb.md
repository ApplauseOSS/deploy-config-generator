<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_pdb

Kubernetes PDB output plugin

### Parameters


#### Deploy config section: kube_pdbs

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`spec`|`dict`|yes||
`spec . max_unavailable`|`int`|no||
`spec . min_available`|`int`|no||
`spec . selector`|`dict`|no||
`spec . selector . match_labels`|`dict`|no||


