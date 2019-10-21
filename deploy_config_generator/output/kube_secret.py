import base64
import copy

from deploy_config_generator.utils import yaml_dump, underscore_to_camelcase
from deploy_config_generator.output import kube_common


class OutputPlugin(kube_common.OutputPlugin):

    NAME = 'kube_secret'
    DESCR = 'Kubernetes secret output plugin'
    FILE_EXT = '.yaml'

    DEFAULT_CONFIG = {
        'fields': {
            'kube_secrets': dict(
                metadata=dict(
                    type='dict',
                    required=True,
                    fields=copy.deepcopy(kube_common.METADATA_FIELD_SPEC),
                ),
                type=dict(
                    type='str',
                    required=True,
                ),
                data=dict(
                    type='dict',
                    description='Values will be automatically base64-encoded as expected by the Kubernetes API',
                ),
                string_data=dict(
                    type='dict',
                ),
            ),
        }
    }

    def generate_output(self, app_vars):
        # Basic structure
        data = {
            'apiVersion': 'v1',
            'kind': 'Secret',
        }
        data['metadata'] = self.build_metadata(app_vars['APP']['metadata'])
        for field in ('type',):
            data[underscore_to_camelcase(field)] = app_vars['APP'][field]
        if app_vars['APP']['string_data']:
            data['stringData'] = app_vars['APP']['string_data']
        if app_vars['APP']['data']:
            tmp_data = dict()
            for key in app_vars['APP']['data']:
                # Values under 'data' should be base64-encoded
                # We have to jump through the hoops of encoding/decoding it because the
                # py3 b64encode() function expects a bytestring, and then the YAML encoder
                # tries to double-encode the resulting bytestring, so we convert it back
                # to a string
                tmp_value = app_vars['APP']['data'][key].encode("utf-8")
                tmp_data[key] = base64.b64encode(tmp_value).decode('utf-8')
            data['data'] = tmp_data

        output = yaml_dump(self._template.render_template(data, app_vars))
        return output
