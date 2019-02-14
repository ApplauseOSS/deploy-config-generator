from deploy_config_generator.output import OutputPluginBase
from deploy_config_generator.utils import json_dump


class OutputPlugin(OutputPluginBase):

    NAME = 'kongfig'
    DESCR = 'Kongfig output plugin'
    FILE_EXT = '.json'

    DEFAULT_CONFIG = {
        'fields': {
            'apps': {
                'proxies': {
                    'description': 'List of Kong API proxy definitions',
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
                                'condition': dict(),
                                'enabled': dict(
                                    type='bool',
                                ),
                            }
                        },
                        'consumers': {
                            'type': 'list',
                            'subtype': 'dict',
                            'fields': {
                                'username': {
                                    'type': 'str',
                                    'required': True,
                                },
                                'custom_id': {
                                    'type': 'str'
                                },
                                'ensure': {
                                    'type': 'str',
                                },
                                'credentials': {
                                    'type': 'list',
                                    'subtype': 'dict',
                                    'fields': {
                                        'name': {
                                            'type': 'str',
                                            'required': True,
                                        },
                                        'ensure': {
                                            'type': 'str',
                                        },
                                        'attributes': {
                                            'type': 'dict',
                                        }
                                    }
                                },
                                'acls': {
                                    'type': 'list',
                                    'subtype': 'dict',
                                    'fields': {
                                        'group': {
                                            'type': 'str',
                                            'required': True,
                                        },
                                        'ensure': {
                                            'type': 'str',
                                        }
                                    }
                                }
                            }
                        }
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
                    tmp_plugin = dict()
                    # Strip out null values
                    for field in plugin:
                        if plugin[field] is not None:
                            tmp_plugin[field] = plugin[field]
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
            # Consumers
            if proxy['consumers']:
                consumers = []
                for consumer in proxy['consumers']:
                    tmp_consumer = dict()
                    # Strip out null values in consumers
                    for field in consumer:
                        if consumer[field] is not None:
                            tmp_consumer[field] = consumer[field]

                    # filter out null values in credentials
                    if consumer['credentials']:
                        tmp_consumer['credentials'] = [dict((k, v) for k, v in creds.items() if v is not None) for creds in consumer['credentials']]

                    # filter out null values in acls
                    if consumer['acls']:
                        tmp_consumer['acls'] = [dict((k, v) for k, v in creds.items() if v is not None) for creds in consumer['acls']]

                    tmp_vars.update(dict(consumer=consumer))
                    consumers.append(tmp_consumer)
                if consumers:
                    tmp_api['consumers'] = consumers
            # Render templates now so that loop vars can be used
            tmp_api = self._template.render_template(tmp_api, tmp_vars)
            data['apis'].append(tmp_api)

        output = json_dump(self._template.render_template(data, app_vars))
        return output
