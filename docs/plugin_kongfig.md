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
`proxies . consumers`|`list` (of `dict`)|no||
`proxies . consumers . acls`|`list` (of `dict`)|no||
`proxies . consumers . acls . ensure`|`str`|no||
`proxies . consumers . acls . group`|`str`|yes||
`proxies . consumers . credentials`|`list` (of `dict`)|no||
`proxies . consumers . credentials . attributes`|`dict`|no||
`proxies . consumers . credentials . ensure`|`str`|no||
`proxies . consumers . credentials . name`|`str`|yes||
`proxies . consumers . custom_id`|`str`|no||
`proxies . consumers . ensure`|`str`|no||
`proxies . consumers . username`|`str`|yes||
`proxies . ensure`|`str`|no||
`proxies . name`||yes||
`proxies . plugins`|`list` (of `dict`)|no||
`proxies . plugins . attributes`|`dict`|no||
`proxies . plugins . condition`||no||
`proxies . plugins . name`||yes||


