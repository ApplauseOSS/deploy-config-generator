<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# dcos_secrets

DC/OS Secrets output plugin (Applause internal)

### Parameters


#### Deploy config section: secrets

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
`name`|`str`|yes||Name of the secret
`terraform_output`|`str`|no||Name of Terraform output to pull secret from
`type`|`str`|no|`password`|Type of secret (password, certificate)


