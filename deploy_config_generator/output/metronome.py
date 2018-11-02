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
                'env': {},
                'user': {},
                'volumes': {},
                'max_launch_delay': {},
                'schedules': {},
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
        # Artifacts
        self.build_artifacts_config(app_vars, data)
        # Schedules
        self.build_schedules_config(app_vars, data)
        # Max launch delay
        if app_vars['APP']['max_launch_delay'] is not None:
            data['run']['maxLaunchDelay'] = int(app_vars['APP']['max_launch_delay'])
        # Volumes
        if app_vars['APP']['volumes'] is not None:
            data['run']['volumes'] = app_vars['APP']['volumes']

        output = json_dump(self._template.render_template(data, app_vars))
        return output

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
