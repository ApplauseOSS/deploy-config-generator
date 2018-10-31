#!/usr/bin/env python

import argparse
import os
import sys
import importlib
import pkgutil

import deploy_config_generator.output as output_ns
from deploy_config_generator.site_config import SiteConfig
from deploy_config_generator.display import Display
from deploy_config_generator.vars import Vars
from deploy_config_generator.errors import DeployConfigError, DeployConfigGenerationError, VarsReplacementError, ConfigError
from deploy_config_generator.utils import yaml_dump, yaml_load, show_traceback

DISPLAY = None


def find_deploy_dir(path):
    if not os.path.isdir(path):
        DISPLAY.display('Path %s is not a directory' % path)
        sys.exit(1)
    deploy_dir = os.path.join(path, 'deploy')
    if not os.path.isdir(deploy_dir):
        DISPLAY.display('Deploy dir could not be found in %s' % path)
        sys.exit(1)
    return deploy_dir


def load_deploy_config(deploy_dir, varset):
    try:
        path = os.path.join(deploy_dir, 'config.yml')
        DISPLAY.v('Loading deploy config file %s' % path)
        yaml_content = ''
        with open(path) as f:
            for line in f:
                yaml_content += varset.replace_vars(line)
        obj = yaml_load(yaml_content)
        # Wrap the config in a list if it's not already a list
        # This makes it easier to process
        if not isinstance(obj, list):
            obj = [ obj ]
        return obj
    except VarsReplacementError as e:
        DISPLAY.display('Failed to load deploy config: %s' % str(e))
        sys.exit(1)


def find_vars_files(path, env):
    ret = []
    vars_dir = os.path.join(path, 'var')
    # TODO: make vars path/files configurable via site config
    for foo in ('defaults.var', '%s.var' % env):
        var_file = os.path.join(vars_dir, foo)
        if os.path.isfile(var_file):
            ret.append(var_file)
    return ret


def load_output_plugins(varset, output_dir):
    plugins = []
    for finder, name, ispkg in pkgutil.iter_modules(output_ns.__path__, output_ns.__name__ + '.'):
        try:
            mod = importlib.import_module(name)
            cls = getattr(mod, 'OutputPlugin')
            plugins.append(cls(varset, output_dir))
        except ConfigError as e:
            DISPLAY.display('Plugin configuration error: %s: %s' % (cls.NAME, str(e)))
            sys.exit(1)
        except Exception as e:
            show_traceback(DISPLAY.get_verbosity())
            DISPLAY.display('Failed to load output plugin %s: %s' % (cls.NAME, str(e)))
            sys.exit(1)
    return plugins


def app_validate_fields(app, app_index, output_plugins):
    try:
        # Validate all fields
        for field in app:
            valid_field = False
            for plugin in output_plugins:
                if plugin.has_field(field) and plugin.is_needed(app):
                    if plugin.is_field_locked(field):
                        DISPLAY.display("The field '%s' has been locked by the plugin config and cannot be overridden" % field)
                        sys.exit(1)
                    valid_field = True
                    break
            if not valid_field:
                raise DeployConfigError("field '%s' in application %d is not valid for relevant output plugins" % (field, app_index + 1))
        # Check for required fields
        for plugin in output_plugins:
            if plugin.is_needed(app):
                req_fields = plugin.get_required_fields()
                for field in req_fields:
                    if field not in app:
                        raise DeployConfigError("required field '%s' not defined" % field)
    except DeployConfigError as e:
        DISPLAY.display('Failed to validate fields in deploy config: %s' % str(e))
        sys.exit(1)


def app_render_output(app, app_index, output_plugins):
    try:
        for plugin in output_plugins:
            if plugin.is_needed(app):
                plugin.generate(app, app_index + 1)
    except DeployConfigGenerationError as e:
        DISPLAY.display('Failed to generate deploy config: %s' % str(e))
        sys.exit(1)


def main():
    global DISPLAY

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        help='Path to service dir',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='Increase verbosity level',
        default=0,
    )
    parser.add_argument(
        '-c', '--config',
        help='Path to config file',
    )
    parser.add_argument(
        '-e', '--env',
        help="Environment to generate deploy configs for (defaults to 'local')",
        default='local'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help="Directory to output generated deploy configs to (defaults to '.')",
        default='.'
    )
    args = parser.parse_args()

    DISPLAY = Display()
    DISPLAY.set_verbosity(args.verbose)

    DISPLAY.vv('Running with args:')
    DISPLAY.vv()
    for arg in dir(args):
        if arg.startswith('_'):
            continue
        DISPLAY.vv('%s: %s' % (arg, getattr(args, arg)))
    DISPLAY.vv()

    config = SiteConfig()
    if args.config:
        try:
            config.load(args.config)
        except ConfigError as e:
            DISPLAY.display('Failed to load site config: %s' % str(e))
            sys.exit(1)

    DISPLAY.vvv('Site config:')
    DISPLAY.vvv()
    DISPLAY.vvv(yaml_dump(config.get_config()))
    DISPLAY.vvv()

    varset = Vars()
    # Load env vars
    varset.update(os.environ)

    output_plugins = load_output_plugins(varset, args.output_dir)

    DISPLAY.vvv('Available output plugins:')
    DISPLAY.vvv()
    for plugin in output_plugins:
        DISPLAY.vvv('- %s (%s)' % (plugin.NAME, plugin.DESCR or 'No description'))
    DISPLAY.vvv()

    deploy_dir = find_deploy_dir(args.path)
    vars_files = find_vars_files(deploy_dir, args.env)

    for vars_file in vars_files:
        DISPLAY.v('Loading vars from %s' % vars_file)
        varset.read_vars_file(vars_file)

    DISPLAY.vvv()
    DISPLAY.vvv('Vars:')
    DISPLAY.vvv()
    DISPLAY.vvv(yaml_dump(dict(varset), default_flow_style=False, indent=2))

    deploy_config = load_deploy_config(deploy_dir, varset)

    DISPLAY.vvv('Deploy config:')
    DISPLAY.vvv()
    DISPLAY.vvv(yaml_dump(deploy_config, default_flow_style=False, indent=2))

    for app_idx, app in enumerate(deploy_config):
        app_validate_fields(app, app_idx, output_plugins)
        app_render_output(app, app_idx, output_plugins)


if __name__ == '__main__':
    main()
