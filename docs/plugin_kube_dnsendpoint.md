<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kube_dnsendpoint

Kubernetes external-dns DNSEndpoint output plugin

### Parameters


#### Deploy config section: kube_dnsendpoints

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`metadata`|`dict`|yes||
`metadata . annotations`|`dict`|no||
`metadata . labels`|`dict`|no||
`metadata . name`|`str`|no||
`metadata . namespace`|`str`|no||
`spec`|`dict`|yes||
`spec . endpoints`|`list` (of `dict`)|yes||
`spec . endpoints . dns_name`|`str`|no||
`spec . endpoints . labels`|`dict`|no||
`spec . endpoints . provider_specific`|`list` (of `dict`)|no||
`spec . endpoints . provider_specific . name`|`str`|no||
`spec . endpoints . provider_specific . value`|`str`|no||
`spec . endpoints . record_TTL`|`int`|no||
`spec . endpoints . record_type`|`str`|no||
`spec . endpoints . targets`|`list` (of `str`)|no||


