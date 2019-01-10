#!/usr/bin/env python

import argparse
import os
import sys
import importlib
import pkgutil
import glob

import deploy_config_generator.output as output_ns
from deploy_config_generator.site_config import SiteConfig
from deploy_config_generator.deploy_config import DeployConfig
from deploy_config_generator.display import Display
from deploy_config_generator.vars import Vars
from deploy_config_generator.template import Template
from deploy_config_generator.errors import DeployConfigError, DeployConfigGenerationError, ConfigError
from deploy_config_generator.utils import yaml_dump, show_traceback

DISPLAY = None
SITE_CONFIG = None


def find_deploy_dir(path):
    '''
    Find directory with deploy config
    '''
    if not os.path.isdir(path):
        DISPLAY.display('Path %s is not a directory' % path)
        sys.exit(1)
    deploy_dir = os.path.join(path, SITE_CONFIG.deploy_dir)
    if not os.path.isdir(deploy_dir):
        DISPLAY.display('Deploy dir could not be found in %s' % path)
        sys.exit(1)
    return deploy_dir


def find_vars_files(path, env):
    '''
    Find vars files that match configured patterns
    '''
    ret = []
    # Evaluate templates in list of patterns
    template = Template()
    tmp_vars = dict(env=env)
    patterns = template.render_template(SITE_CONFIG.vars_file_patterns, tmp_vars)
    # Find files matching list of patterns
    vars_dir = os.path.join(path, SITE_CONFIG.vars_dir)
    for pattern in patterns:
        matches = glob.glob(os.path.join(vars_dir, pattern))
        for var_file in matches:
            if os.path.isfile(var_file):
                ret.append(var_file)
    return ret


def load_output_plugins(varset, output_dir):
    '''
    Find, import, and instantiate all output plugins
    '''
    plugins = []
    for finder, name, ispkg in pkgutil.iter_modules(output_ns.__path__, output_ns.__name__ + '.'):
        try:
            mod = importlib.import_module(name)
            cls = getattr(mod, 'OutputPlugin')
            DISPLAY.v('Loading plugin %s' % cls.NAME)
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
        unmatched = None
        plugins_used = []
        for plugin in output_plugins:
            if plugin.is_needed(app):
                plugins_used.append(plugin.NAME)
                plugin_unmatched = plugin.validate_fields(app)
                if unmatched is not None:
                    # Set to intersection of previous unmatched and current unmatched
                    # The idea is to end up with a list of fields that were unmatched in all
                    # active output plugins
                    unmatched = list(set(unmatched) & set(plugin_unmatched))
                else:
                    unmatched = plugin_unmatched
        if unmatched:
            raise DeployConfigError('found the following unknown fields: %s' % ', '.join(sorted(unmatched)))
        if not plugins_used:
            raise DeployConfigError('no output plugins were available for provided fields')
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
    global DISPLAY, SITE_CONFIG

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

    SITE_CONFIG = SiteConfig()
    if args.config:
        try:
            SITE_CONFIG.load(args.config)
        except ConfigError as e:
            DISPLAY.display('Failed to load site config: %s' % str(e))
            sys.exit(1)

    DISPLAY.vvvv('Site config:')
    DISPLAY.vvvv()
    DISPLAY.vvvv(yaml_dump(SITE_CONFIG.get_config()))
    DISPLAY.vvvv()

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

    DISPLAY.vvvv()
    DISPLAY.vvvv('Vars:')
    DISPLAY.vvvv()
    DISPLAY.vvvv(yaml_dump(dict(varset), default_flow_style=False, indent=2))

    try:
        deploy_config = DeployConfig(os.path.join(deploy_dir, SITE_CONFIG.deploy_config_file), varset)
    except DeployConfigError as e:
        DISPLAY.display('Error loading deploy config: %s' % str(e))
        sys.exit(1)

    DISPLAY.vvvv('Deploy config:')
    DISPLAY.vvvv()
    DISPLAY.vvvv(yaml_dump(deploy_config.get_config(), default_flow_style=False, indent=2))

    for section in deploy_config.get_config():
        for plugin in output_plugins:
            plugin.set_section(section)
        for app_idx, app in enumerate(deploy_config.get_config()[section]):
            app_validate_fields(app, app_idx, output_plugins)
            app_render_output(app, app_idx, output_plugins)


if __name__ == '__main__':
    main()
