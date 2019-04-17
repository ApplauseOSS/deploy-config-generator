# deploy-config-generator

Utility for generating deployment configs for a service

* [Basic usage](#basic-usage)
* [The dirty details](#the-dirty-details)
  * [Site config](#site-config)
    * [Global options](#global-options)
  * [Variables](#variables)
  * [Deploy config](#deploy-config)
  * [Plugins](#plugins)
* [Development](#development)
  * [Running tests](#running-tests)
  * [Regenerating plugin docs](#regenerating-plugin-docs)

## Basic usage

The below command will generate the required deployment config files for the specified service in the current directory.

```bash
$ deploy-config-generator path/to/service/repo
```

You can specify the environment to generate configuration for.

```bash
$ deploy-config-generator path/to/service/repo -e stage
```

You can specify the output directory using the `--output-dir` option.

```bash
$ deploy-config-generator path/to/service/repo --output-dir /tmp
```

You can increase the verbosity level to see what the script is doing.

```bash
$ deploy-config-generator path/to/service/repo -vvv
```

You can specify the path to a site config file.

```bash
$ deploy-config-generator path/to/service/repo --config path/to/site/config.yml
```

## The dirty details

### Site config

The optional site config file is expected to be a YAML file with the following basic structure.

```yaml
---
some_global_option: foo
another_global_option: bar
plugins:
  plugin_name:
    some_plugin_option: baz
    fields:
      <field definitions>
```

The field definitions should have the following basic structure (continued from above).

```yaml
    fields:
      field_name1:
        type: str
      field_name2:
        type: bool
        default: false
```

#### Global options

The following global options are available.

Name | Default | Description
--- | --- | ---
`default_output` | | The default output plugin to use (probably to be removed)
`deploy_dir` | `deploy` | Directory within service dir where deploy config is located
`deploy_config_file` | `config.yml` | Name of deploy config file
`vars_dir` | `var` | Directory within deploy dir to look for vars files
`local_vars_file_patterns` | `['local.var']` | Patterns for finding "local" vars files
`defaults_vars_file_patterns` | `['defaults.var']` | Patterns for finding "defaults" vars files
`env_vars_file_patterns` | `['{{ env }}.var', 'env_{{ env }}.var']` | Patterns for finding env-specific vars files
`use_env_vars` | `True` | Whether to read vars from environment
`plugin_dirs` | `[]` | Additional dirs where plugins can be found

### Variables

Variables are read from shell-compatible `.var` files (by default) located in the deploy directory. Variable
definitions referencing other variables (using the `$FOO` or `${FOO}` notation) are supported, except for with the
"local" vars file. Vars are read in the following order.

* "local" vars file(s) - used as stand-in values when vars that normally come from the environment
  are not present
* vars from environment - useful for running in a CI job
* "defaults" vars file(s) - default values for all environments
* env-specific vars files - values specific to a particular application environment

### Deploy config

The deploy config is read from `deploy/config.yml` (by default) from the directory specified on the
commandline. It is expected to be a YAML file with the following basic structure.

```yaml
---
apps:
  <app definitions>
jobs:
  <job definitions>
```

The available top-level sections and the keys allowed for them are defined by the individual output
plugins.

### Plugins

This tool uses a plugin system for handling the generation of deploy files for various backends.

The following output plugins are available:

* [`marathon`](docs/plugin_marathon.md)
* [`metronome`](docs/plugin_metronome.md)
* [`kongfig`](docs/plugin_kongfig.md)
* [`dummy`](docs/plugin_dummy.md)

## Development

### Running tests

This tool comes with unit and integration test suites, which can be run with the commands:

```bash
$ python setup.py test
$ python setup.py integration
```

You can run the full test suite in multiple python versions using `tox` by running:

```bash
$ tox
```

### Regenerating plugin docs

The docs for the individual plugins are generated from the code of the plugins. You can regenerate the plugin docs
with the following command:

```bash
$ scripts/gen-plugin-docs.py
```
