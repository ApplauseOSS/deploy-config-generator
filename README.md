# applause-deploy-config-generator

Utility for generating deployment configs for an Applause service

## Basic Usage

The below command will generate the required deployment config files for the specified service in the current directory.

```bash
$ applause-deploy-config-generator path/to/service/repo
```

You can specify the output directory using the `--output-dir` option.

```bash
$ applause-deploy-config-generator path/to/service/repo --output-dir /tmp
```

You can increase the verbosity level to see what the script is doing.

```bash
$ applause-deploy-config-generator path/to/service/repo -vvv
```

## Running Tests

This tool comes with a unit test suite, which can be run with the command:

```bash
$ python setup.py test
```
