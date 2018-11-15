from deploy_config_generator.output import OutputPluginBase
from deploy_config_generator.utils import yaml_dump


class OutputPlugin(OutputPluginBase):

    NAME = 'kongfig'
    DESCR = 'Kongfig output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'apps': {
                'proxies': {
                    'required': True,
                    'type': 'list',
                    'subtype': 'dict',
                    'fields': {
                        'name': {
                            'required': True,
                        },
                        'ensure': {
                            'type': 'str',
                        },
                        'attributes': {
                            'type': 'dict',
                        },
                        'plugins': {
                            'type': 'list',
                            'subtype': 'dict',
                            'fields': {
                                'name': {
                                    'required': True,
                                },
                                'attributes': {
                                    'type': 'dict',
                                },
                            }
                        },
                    },
                },
            }
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apis': [],
        }
        for proxy in app_vars['APP']['proxies']:
            tmp_api = {
                'name': proxy['name'],
            }
            tmp_vars = app_vars.copy()
            tmp_vars.update(dict(proxy=proxy))
            # Ensure
            if proxy['ensure'] is not None:
                tmp_api['ensure'] = proxy['ensure']
            # Attributes
            if proxy['attributes']:
                tmp_api['attributes'] = proxy['attributes']
            # Plugins
            if proxy['plugins']:
                plugins = []
                for plugin in proxy['plugins']:
                    tmp_plugin = plugin.copy()
                    tmp_vars.update(dict(plugin=plugin))
                    if 'condition' in tmp_plugin:
                        # Only include plugin if conditional evaluates to True
                        if self._template.evaluate_condition(plugin['condition'], tmp_vars):
                            plugins.append(tmp_plugin)
                        # Remove 'condition' key so it doesn't appear in generated output
                        del tmp_plugin['condition']
                    else:
                        plugins.append(tmp_plugin)
                if plugins:
                    tmp_api['plugins'] = plugins
            data['apis'].append(tmp_api)

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
