import copy

from deploy_config_generator.utils import yaml_dump
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_cronjob'
    DESCR = 'Kubernetes cronjob output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_cronjobs': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                spec=dict(
                    type='dict',
                    required=True,
                    fields=dict(
                        concurrency_policy=dict(
                            type='str',
                        ),
                        failed_jobs_history_limit=dict(
                            type='int',
                        ),
                        job_template=dict(
                            type='dict',
                            required=True,
                            fields=dict(
                                metadata=dict(
                                    type='dict',
                                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                                ),
                                spec=dict(
                                    type='dict',
                                    required=True,
                                    fields=copy.deepcopy(kube_common.JOB_SPEC_FIELD_SPEC),
                                ),
                            ),
                        ),
                        schedule=dict(
                            type='str',
                            required=True,
                        ),
                        starting_deadline_seconds=dict(
                            type='int',
                        ),
                        successful_jobs_history_limit=dict(
                            type='int',
                        ),
                        suspend=dict(
                            type='bool',
                        ),
                    )
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'batch/v1beta1',
            'kind': 'CronJob',
            'spec': dict(),
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        data['spec'] = self.build_generic(app_vars['APP']['spec'], self._plugin_config['fields']['kube_cronjobs']['spec']['fields'])

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
