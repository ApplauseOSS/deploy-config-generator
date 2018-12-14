#!/usr/bin/env python

import sys
import os
import argparse
import importlib
import pkgutil

# Needed to find libraries
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..'))

import deploy_config_generator.output as output_ns
from deploy_config_generator.site_config import SiteConfig
from deploy_config_generator.display import Display
from deploy_config_generator.vars import Vars
from deploy_config_generator.template import Template
from deploy_config_generator.errors import ConfigError
from deploy_config_generator.utils import show_traceback

DISPLAY = None
SITE_CONFIG = None

PLUGIN_DOC_TEMPLATE = r'''
{%- macro cleanup(value) -%}
{{ value | regex_replace('[|]', '\|') }}
{%- endmacro -%}
<!--
NOTE: this document is automatically generated. Any manual changes will get overwritten.
-->
# {{ plugin.NAME }}

{{ plugin.DESCR }}

### Parameters

{% for section in fields %}
#### Deploy config section: {{ section }}

Name | Type | Required | Default | Description
--- | --- | --- | --- | ---
{%- for field in fields[section] %}
`{{ field.get_full_name().split('.') | join(' . ') }}`
{#- Chomp whitespace between fields -#}
|{% if field.type %}`{{ field.type }}`{% if field.subtype %} (of `{{ field.subtype }}`){% endif %}{% endif %}
{#- Chomp whitespace between fields -#}
|{{ 'yes' if field.required else 'no' }}
{#- Chomp whitespace between fields -#}
|{% if field.default is not none %}`{{ cleanup(field.default) }}`{% endif %}
{#- Chomp whitespace between fields -#}
|{{ field.description | default('') }}
{%- endfor %}

{% endfor %}
'''


def load_output_plugins(varset):
    '''
    Find/import all output plugins
    '''
    plugins = []
    for finder, name, ispkg in pkgutil.iter_modules(output_ns.__path__, output_ns.__name__ + '.'):
        try:
            mod = importlib.import_module(name)
            cls = getattr(mod, 'OutputPlugin')
            plugins.append(cls(varset, ''))
        except Exception as e:
            show_traceback(DISPLAY.get_verbosity())
            DISPLAY.display('Failed to load output plugin %s: %s' % (cls.NAME, str(e)))
            sys.exit(1)
    return plugins


def get_plugin_fields(fields):
    '''
    Create sorted list of nested fields
    '''
    ret = []
    for field_name in sorted(fields.keys()):
        field = fields[field_name]
        ret.append(field)
        if field.fields:
            ret.extend(get_plugin_fields(field.fields))
    return ret


def main():
    global DISPLAY, SITE_CONFIG

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        help='Path to config file',
    )
    parser.add_argument(
        '-o', '--output-dir',
        help="Directory to output generated docs to (defaults to '../docs')",
        default='../docs'
    )
    args = parser.parse_args()

    DISPLAY = Display()
    # Verbosity of 3 is needed for displaying tracebacks
    DISPLAY.set_verbosity(3)

    SITE_CONFIG = SiteConfig()
    if args.config:
        try:
            SITE_CONFIG.load(args.config)
        except ConfigError as e:
            DISPLAY.display('Failed to load site config: %s' % str(e))
            sys.exit(1)

    # Needed for instantiating output plugin classes
    varset = Vars()

    # Disable recursive variable lookups to avoid rendering templates
    # in field defaults from the site config
    tmpl = Template(recursive=False)

    output_plugins = load_output_plugins(varset)
    for plugin in output_plugins:
        tmp_fields = dict()
        for section in plugin._fields:
            tmp_fields[section] = get_plugin_fields(plugin._fields[section])
        tmp_vars = dict(
            plugin=plugin,
            fields=tmp_fields,
        )
        output_file = os.path.join(os.path.dirname(__file__), args.output_dir, 'plugin_%s.md' % plugin.NAME)
        DISPLAY.display('Writing file %s' % output_file)
        with open(output_file, 'w') as f:
            f.write(tmpl.render_template(PLUGIN_DOC_TEMPLATE, tmp_vars))


if __name__ == '__main__':
    main()
