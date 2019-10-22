import copy

from deploy_config_generator.utils import yaml_dump, underscore_to_camelcase
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_deployment'
    DESCR = 'Kubernetes deployment output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_deployments': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    required=True,
                    fields=dict(
                        min_ready_seconds=dict(
                            type='int',
                        ),
                        paused=dict(
                            type='bool',
                        ),
                        progress_deadline_seconds=dict(
                            type='int',
                        ),
                        replicas=dict(
                            type='int',
                        ),
                        revision_history_limit=dict(
                            type='int',
                        ),
                        selector=dict(
                            type='dict',
                            required=True,
                            fields=copy.deepcopy(kube_common.SELECTOR_FIELD_SPEC),
                        ),
                        strategy=dict(
                            type='dict',
                            fields=dict(
                                rolling_update=dict(
                                    type='dict',
                                    fields=dict(
                                        max_surge=dict(
                                            type='str',
                                        ),
                                        max_unavailable=dict(
                                            type='str',
                                        ),
                                    ),
                                ),
                                type=dict(
                                    type='str',
                                ),
                            ),
                        ),
                        template=dict(
                            type='dict',
                            required=True,
                            fields=copy.deepcopy(kube_common.POD_TEMPLATE_FIELD_SPEC),
                        ),
                    ),
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'spec': dict(),
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        self.build_spec(app_vars, data)

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output

    def build_spec(self, app_vars, data):
        for field in ('min_ready_seconds', 'paused', 'progress_deadline_seconds', 'replicas', 'revision_history_limit'):
            if app_vars['APP']['spec'][field] is not None:
                data['spec'][underscore_to_camelcase(field)] = app_vars['APP']['spec'][field]
        self.build_spec_selector(app_vars, data)
        self.build_spec_strategy(app_vars, data)
        self.build_spec_template(app_vars, data)

    def build_spec_selector(self, app_vars, data):
        tmp_selector = dict()
        for field in ('match_expressions', 'match_labels'):
            if app_vars['APP']['spec']['selector'][field]:
                tmp_selector[underscore_to_camelcase(field)] = app_vars['APP']['spec']['selector'][field]
        if tmp_selector:
            data['spec']['selector'] = tmp_selector

    def build_spec_strategy(self, app_vars, data):
        tmp_strategy = dict()
        if app_vars['APP']['spec']['strategy']['type'] is not None:
            tmp_strategy['type'] = app_vars['APP']['spec']['strategy']['type']
        if app_vars['APP']['spec']['strategy']['rolling_update']:
            tmp_rolling_update = dict()
            for field in ('max_surge', 'max_unavailable'):
                if app_vars['APP']['spec']['strategy']['rolling_update'].get(field, None) is not None:
                    tmp_rolling_update[underscore_to_camelcase(field)] = app_vars['APP']['spec']['strategy']['rolling_update'][field]
            if tmp_rolling_update:
                tmp_strategy['rollingUpdate'] = tmp_rolling_update
        if tmp_strategy:
            data['spec']['strategy'] = tmp_strategy

    def build_spec_template(self, app_vars, data):
        data['spec']['template'] = self.build_pod_template(app_vars['APP']['spec']['template'])
