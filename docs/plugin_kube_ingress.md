<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_ingress

Kubernetes ingress output plugin

### Parameters


#### Deploy config section: kube_ingresses

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`spec`|`dict`|yes||
`spec . backend`|`dict`|no||
`spec . backend . service_name`|`str`|no||
`spec . backend . service_port`||no||
`spec . rules`|`list` (of `dict`)|no||
`spec . rules . host`|`str`|no||
`spec . rules . http`|`dict`|no||
`spec . rules . http . paths`|`list` (of `dict`)|no||
`spec . rules . http . paths . backend`|`dict`|no||
`spec . rules . http . paths . backend . service_name`|`str`|no||
`spec . rules . http . paths . backend . service_port`||no||
`spec . rules . http . paths . path`|`str`|no||
`spec . tls`|`list` (of `dict`)|no||
`spec . tls . host`|`list` (of `str`)|no||
`spec . tls . secret_name`|`str`|no||


