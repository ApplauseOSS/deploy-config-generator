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
`spec . default_backend`|`dict`|no||
`spec . default_backend . resource`|`dict`|no||
`spec . default_backend . resource . api_group`|`str`|no||
`spec . default_backend . resource . kind`|`str`|no||
`spec . default_backend . resource . name`|`str`|no||
`spec . default_backend . service`|`dict`|no||
`spec . default_backend . service . name`|`str`|no||
`spec . default_backend . service . port`|`dict`|no||
`spec . default_backend . service . port . name`|`str`|no||
`spec . default_backend . service . port . number`|`int`|no||
`spec . rules`|`list` (of `dict`)|no||
`spec . rules . host`|`str`|no||
`spec . rules . http`|`dict`|no||
`spec . rules . http . paths`|`list` (of `dict`)|no||
`spec . rules . http . paths . backend`|`dict`|no||
`spec . rules . http . paths . backend . resource`|`dict`|no||
`spec . rules . http . paths . backend . resource . api_group`|`str`|no||
`spec . rules . http . paths . backend . resource . kind`|`str`|no||
`spec . rules . http . paths . backend . resource . name`|`str`|no||
`spec . rules . http . paths . backend . service`|`dict`|no||
`spec . rules . http . paths . backend . service . name`|`str`|no||
`spec . rules . http . paths . backend . service . port`|`dict`|no||
`spec . rules . http . paths . backend . service . port . name`|`str`|no||
`spec . rules . http . paths . backend . service . port . number`|`int`|no||
`spec . rules . http . paths . path`|`str`|no||
`spec . rules . http . paths . path_type`|`str`|yes||
`spec . tls`|`list` (of `dict`)|no||
`spec . tls . host`|`list` (of `str`)|no||
`spec . tls . secret_name`|`str`|no||


