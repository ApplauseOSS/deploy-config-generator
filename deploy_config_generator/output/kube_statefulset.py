import copy

from deploy_config_generator.utils import yaml_dump, underscore_to_camelcase
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_statefulset'
    DESCR = 'Kubernetes statefulset output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_statefulsets': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    required=True,
                    fields=dict(
                        pod_management_policy=dict(
                            type='str',
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
                        service_name=dict(
                            type='str',
                            required=True,
                        ),
                        template=dict(
                            type='dict',
                            required=True,
                            fields=copy.deepcopy(kube_common.POD_TEMPLATE_FIELD_SPEC),
                        ),
                        update_strategy=dict(
                            type='dict',
                            fields=dict(
                                rolling_update=dict(
                                    type='dict',
                                    fields=dict(
                                        partition=dict(
                                            type='int',
                                        ),
                                    ),
                                ),
                                type=dict(
                                    type='str',
                                ),
                            ),
                        ),
                        volume_claim_templates=dict(
                            type='list',
                            subtype='dict',
                            fields=dict(
                                metadata=dict(
                                    type='dict',
                                    required=True,
                                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                                ),
                                spec=dict(
                                    type='dict',
                                    required=True,
                                    fields=copy.deepcopy(kube_common.PERSISTENT_VOLUME_CLAIM_FIELD_SPEC),
                                ),
                            ),
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
            'kind': 'StatefulSet',
            'spec': dict(
            ),
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        self.build_spec(app_vars, data)

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output

    def build_spec(self, app_vars, data):
        for field in ('pod_management_policy', 'replicas', 'revision_history_limit', 'service_name'):
            if app_vars['APP']['spec'][field] is not None:
                data['spec'][underscore_to_camelcase(field)] = app_vars['APP']['spec'][field]
        self.build_spec_selector(app_vars, data)
        self.build_spec_update_strategy(app_vars, data)
        self.build_spec_template(app_vars, data)
        self.build_spec_volume_claim(app_vars, data)

    def build_spec_selector(self, app_vars, data):
        tmp_selector = dict()
        for field in ('match_expressions', 'match_labels'):
            if app_vars['APP']['spec']['selector'][field]:
                tmp_selector[underscore_to_camelcase(field)] = app_vars['APP']['spec']['selector'][field]
        if tmp_selector:
            data['spec']['selector'] = tmp_selector

    def build_spec_update_strategy(self, app_vars, data):
        tmp_strategy = dict()
        if app_vars['APP']['spec']['update_strategy']['type']:
            tmp_strategy['type'] = app_vars['APP']['spec']['update_strategy']['type']
        if app_vars['APP']['spec']['update_strategy']['rolling_update']['partition'] is not None:
            tmp_strategy['rollingUpdate'] = dict(partition=app_vars['APP']['spec']['update_strategy']['rolling_update']['partition'])
        if tmp_strategy:
            data['spec']['updateStrategy'] = tmp_strategy

    def build_spec_template(self, app_vars, data):
        data['spec']['template'] = self.build_pod_template(app_vars['APP']['spec']['template'])

    def build_spec_volume_claim(self, app_vars, data):
        tmp_claims = []
        if app_vars['APP']['spec']['volume_claim_templates']:
            for claim in app_vars['APP']['spec']['volume_claim_templates']:
                tmp_claim = dict(
                    metadata=self.build_metadata(claim['metadata']),
                    spec=dict(),
                )
                tmp_claim['spec'] = self.build_generic(claim['spec'], self._fields['kube_statefulsets']['spec']['fields']['volume_claim_templates']['fields']['spec']['fields'])
            tmp_claims.append(tmp_claim)
        if tmp_claims:
            data['spec']['volumeClaimTemplates'] = tmp_claims
