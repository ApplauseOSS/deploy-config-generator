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
from deploy_config_generator.errors import DeployConfigError, DeployConfigGenerationError, ConfigError, VarsReplacementError
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


def load_vars(varset, deploy_dir, env='BAD_VALUE_NO_MATCH'):
    vars_path = os.path.join(deploy_dir, SITE_CONFIG.vars_dir)

    # Used for replacing vars in file patterns
    template = Template()
    tmp_vars = dict(env=env)

    # Load "local" vars
    load_vars_files(varset, vars_path, template.render_template(SITE_CONFIG.local_vars_file_patterns, tmp_vars), allow_var_references=False)

    # Load env vars
    if SITE_CONFIG.use_env_vars:
        DISPLAY.v('Loading vars from environment')
        varset.update(os.environ)

    # Load "defaults" vars
    load_vars_files(varset, vars_path, template.render_template(SITE_CONFIG.defaults_vars_file_patterns, tmp_vars))

    # Load env-specific vars
    load_vars_files(varset, vars_path, template.render_template(SITE_CONFIG.env_vars_file_patterns, tmp_vars))


def load_vars_files(varset, vars_dir, patterns, allow_var_references=True):
    '''
    Find vars files that match configured patterns
    '''
    vars_files = []
    # Find files matching list of patterns
    for pattern in patterns:
        matches = glob.glob(os.path.join(vars_dir, pattern))
        for var_file in matches:
            if os.path.isfile(var_file):
                vars_files.append(var_file)
    for vars_file in vars_files:
        DISPLAY.v('Loading vars from %s' % vars_file)
        varset.read_vars_file(vars_file, allow_var_references=allow_var_references)


def load_output_plugins(varset, output_dir, config_version):
    '''
    Find, import, and instantiate all output plugins
    '''
    plugins = []
    for plugin_dir in (output_ns.__path__ + SITE_CONFIG.plugin_dirs):
        DISPLAY.vv('Looking in plugin dir %s' % plugin_dir)
        sys.path.insert(0, plugin_dir)
        for finder, name, ispkg in pkgutil.iter_modules([plugin_dir]):
            try:
                mod = importlib.import_module(name)
                cls = getattr(mod, 'OutputPlugin')
                DISPLAY.v('Loading plugin %s' % cls.NAME)
                plugins.append(cls(varset, output_dir, config_version))
            except ConfigError as e:
                DISPLAY.display('Plugin configuration error: %s: %s' % (cls.NAME, str(e)))
                sys.exit(1)
            except Exception as e:
                show_traceback(DISPLAY.get_verbosity())
                DISPLAY.display('Failed to load output plugin %s: %s' % (cls.NAME, str(e)))
                sys.exit(1)
        sys.path.pop(0)
    return plugins


def app_validate_fields(app, app_index, output_plugins):
    try:
        unmatched = {}
        plugins_used = []
        for plugin in output_plugins:
            if plugin.is_needed(app):
                plugins_used.append(plugin.NAME)
                plugin_unmatched = plugin.validate_fields(app)
                unmatched[plugin.NAME] = plugin_unmatched
        # Compare unmatched from all plugins and compile final list
        # We are looking for fields that were unmatched by all active plugins,
        # with the added twist that we need to match what may be an unmatched
        # sub-field in one plugin and a top-level field in another.
        final_unmatched = []
        for plugin in unmatched:
            for entry in unmatched[plugin]:
                entry_keep = True
                # Check entry against unmatched entries from other plugins
                for plugin2 in unmatched:
                    if plugin2 == plugin:
                        continue
                    plugin2_matched = False
                    for entry2 in unmatched[plugin2]:
                        # Check for exact match or a parent/sub-field match
                        if entry2 == entry or entry.startswith('%s.' % entry2):
                            plugin2_matched = True
                            break
                    if not plugin2_matched:
                        entry_keep = False
                        break
                # Add entry to final list if it existed for all plugins
                if entry_keep and entry not in final_unmatched:
                    final_unmatched.append(entry)
        if final_unmatched:
            raise DeployConfigError('found the following unknown fields: %s' % ', '.join(sorted(final_unmatched)))
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
        help="Environment to generate deploy configs for",
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
    if args.config is None:
        # Possible config locations
        config_paths = [
            os.path.join(os.environ.get('HOME', None), '.deploy-config-generator-site.yml'),
        ]
        for path in config_paths:
            if os.path.exists(path):
                args.config = path
                break
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
    varset['env'] = args.env

    deploy_dir = find_deploy_dir(args.path)

    try:
        load_vars(varset, deploy_dir, args.env)
    except Exception as e:
        DISPLAY.display('Error loading vars: %s' % str(e))
        show_traceback(DISPLAY.get_verbosity())
        sys.exit(1)

    DISPLAY.vvvv()
    DISPLAY.vvvv('Vars:')
    DISPLAY.vvvv()
    DISPLAY.vvvv(yaml_dump(dict(varset), default_flow_style=False, indent=2))

    try:
        deploy_config = DeployConfig(os.path.join(deploy_dir, SITE_CONFIG.deploy_config_file), varset)
        deploy_config.set_config(varset.replace_vars(deploy_config.get_config()))
    except DeployConfigError as e:
        DISPLAY.display('Error loading deploy config: %s' % str(e))
        show_traceback(DISPLAY.get_verbosity())
        sys.exit(1)
    except VarsReplacementError as e:
        DISPLAY.display('Error loading deploy config: variable replacement error: %s' % str(e))
        show_traceback(DISPLAY.get_verbosity())
        sys.exit(1)

    DISPLAY.vvvv('Deploy config:')
    DISPLAY.vvvv()
    DISPLAY.vvvv(yaml_dump(deploy_config.get_config(), default_flow_style=False, indent=2))

    deploy_config_version = deploy_config.get_version() or SITE_CONFIG.default_config_version
    output_plugins = load_output_plugins(varset, args.output_dir, deploy_config_version)

    DISPLAY.vvv('Available output plugins:')
    DISPLAY.vvv()
    valid_sections = []
    for plugin in output_plugins:
        DISPLAY.vvv('- %s (%s)' % (plugin.NAME, plugin.DESCR or 'No description'))
        valid_sections += plugin._fields.keys()
    DISPLAY.vvv()

    try:
        deploy_config.apply_default_apps(SITE_CONFIG.default_apps)
        deploy_config.validate_sections(valid_sections)
    except DeployConfigError as e:
        DISPLAY.display('Error validating deploy config: %s' % str(e))
        sys.exit(1)

    for section in deploy_config.get_config():
        for plugin in output_plugins:
            plugin.set_section(section)
        for app_idx, app in enumerate(deploy_config.get_config()[section]):
            app_validate_fields(app, app_idx, output_plugins)
            app_render_output(app, app_idx, output_plugins)


if __name__ == '__main__':
    main()
