from deploy_config_generator.utils import json_dump
from deploy_config_generator.output import OutputPluginBase


class OutputPlugin(OutputPluginBase):

    NAME = 'metronome'
    DESCR = 'Metronome output plugin'
    FILE_EXT = '.json'

    DEFAULT_CONFIG = {
        'fields': {
            'jobs': {
                'id': dict(
                    required=True
                ),
                'cpus': dict(
                    required=True
                ),
                'mem': dict(
                    required=True
                ),
                'disk': dict(
                    required=True
                ),
                'cmd': dict(
                    required=True
                ),
                'description': {},
                'docker_image': {},
                'artifacts': {},
                'labels': {},
                'env': dict(
                    type='dict',
                ),
                'user': {},
                'volumes': {},
                'max_launch_delay': {},
                'schedules': {},
                'restart': dict(
                    type='dict',
                    fields=dict(
                        policy=dict(
                            required=True,
                        ),
                        active_deadline_seconds=dict(
                            type='int',
                        ),
                    ),
                ),
                'secrets': dict(
                    description='List of secrets from the DC/OS secret store',
                    type='list',
                    subtype='dict',
                    fields=dict(
                        name=dict(
                            required=True,
                            description='Name of secret to expose for env/volumes',
                        ),
                        source=dict(
                            required=True,
                            description='Name of secret in DC/OS secret store',
                        ),
                    ),
                ),
            }
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'id': '{{ APP.id }}',
            'run': {
                'cpus': '{{ APP.cpus | output_float }}',
                'mem': '{{ APP.mem | output_int }}',
                'disk': '{{ APP.disk | output_int }}',
                'cmd': '{{ APP.cmd }}',
            }
        }
        # Description
        if app_vars['APP']['description'] is not None:
            data['description'] = app_vars['APP']['description']
        # Labels
        if app_vars['APP']['labels'] is not None:
            data['labels'] = app_vars['APP']['labels']
        # Docker image
        if app_vars['APP']['docker_image'] is not None:
            data['run']['docker'] = { 'image': app_vars['APP']['docker_image'] }
        # Environment vars
        if app_vars['APP']['env'] is not None:
            data['run']['env'] = app_vars['APP']['env']
        # Secrets
        self.build_secrets(app_vars, data)
        # Artifacts
        self.build_artifacts_config(app_vars, data)
        # Schedules
        self.build_schedules_config(app_vars, data)
        # Restart policy
        self.build_restart_policy(app_vars, data)
        # Max launch delay
        if app_vars['APP']['max_launch_delay'] is not None:
            data['run']['maxLaunchDelay'] = int(app_vars['APP']['max_launch_delay'])
        # Volumes
        if app_vars['APP']['volumes'] is not None:
            data['run']['volumes'] = app_vars['APP']['volumes']

        output = json_dump(self._template.render_template(data, app_vars))
        return output

    def build_secrets(self, app_vars, data):
        if app_vars['APP']['secrets']:
            secrets = {}
            tmp_vars = app_vars.copy()
            for secret_index, secret in enumerate(app_vars['APP']['secrets']):
                tmp_vars.update(dict(secret=secret, secret_index=secret_index))
                tmp_secret = {
                    'source': secret['source']
                }
                if tmp_secret:
                    tmp_secret = self._template.render_template(tmp_secret, tmp_vars)
                    secrets[secret['name']] = tmp_secret
            if secrets:
                data['run']['secrets'] = secrets

    def build_restart_policy(self, app_vars, data):
        if app_vars['APP']['restart']:
            tmp_restart = {}
            if app_vars['APP']['restart']['policy'] is not None:
                tmp_restart['policy'] = app_vars['APP']['restart']['policy']
            if app_vars['APP']['restart']['active_deadline_seconds'] is not None:
                tmp_restart['activeDeadlineSeconds'] = int(app_vars['APP']['restart']['active_deadline_seconds'])
            if tmp_restart:
                data['run']['restart'] = tmp_restart

    def build_artifacts_config(self, app_vars, data):
        if app_vars['APP']['artifacts'] is not None:
            tmp_vars = app_vars.copy()
            artifacts_config = []
            for artifact_index, artifact in enumerate(app_vars['APP']['artifacts']):
                tmp_vars.update(dict(artifact=artifact, artifact_index=artifact_index))
                if not ('condition' in artifact) or self._template.evaluate_condition(artifact['condition'], tmp_vars):
                    tmp_artifact = artifact.copy()
                    if 'condition' in tmp_artifact:
                        del tmp_artifact['condition']
                    artifacts_config.append(tmp_artifact)
            if artifacts_config:
                data['run']['artifacts'] = artifacts_config

    def build_schedules_config(self, app_vars, data):
        if app_vars['APP']['schedules'] is not None:
            tmp_vars = app_vars.copy()
            schedules_config = []
            for schedule_index, schedule in enumerate(app_vars['APP']['schedules']):
                tmp_vars.update(dict(schedule=schedule, schedule_index=schedule_index))
                if not ('condition' in schedule) or self._template.evaluate_condition(schedule['condition'], tmp_vars):
                    tmp_schedule = schedule.copy()
                    if 'condition' in tmp_schedule:
                        del tmp_schedule['condition']
                    schedules_config.append(tmp_schedule)
            if schedules_config:
                data['schedules'] = schedules_config
