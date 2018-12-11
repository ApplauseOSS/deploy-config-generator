<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# kongfig

Kongfig output plugin

### Parameters


#### Deploy config section: apps

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`proxies`|`list` (of `dict`)|yes||List of Kong API proxy definitions
`proxies . attributes`|`dict`|no||
`proxies . ensure`|`str`|no||
`proxies . name`||yes||
`proxies . plugins`|`list` (of `dict`)|no||
`proxies . plugins . attributes`|`dict`|no||
`proxies . plugins . condition`||no||
`proxies . plugins . name`||yes||

