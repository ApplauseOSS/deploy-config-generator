from deploy_config_generator.output import OutputPluginBase

_TEMPLATE = '''
{
  "id": "{{ CONFIG.group }}/{{ CONFIG.name }}",
  "cpus": {{ CONFIG.cpus }},
  "mem": {{ CONFIG.mem }},
  "disk": {{ CONFIG.disk }},
  "instances": {{ CONFIG.instances }},
  "constraints": [
    [ "@region", "IS", "aws/us-east-1" ],
    [ "@zone", "GROUP_BY", "{{ CONFIG.num_azs }}" ]
  ],
  "container": {
    "type": "DOCKER",
    "volumes": [],
    "docker": {
      "image": "{{ CONFIG.image }}",
      "network": "BRIDGE",
{%- if CONFIG.ports is defined %}
      "portMappings": [
{%-   for port in CONFIG.ports %}
        {
          "containerPort": {{ port.container_port }},
          "hostPort": 0,
          "servicePort": 0,
          "protocol": "tcp",
          "labels": {
{%-     if port.vip_port is defined %}
            "VIP_0": "/{{ CONFIG.group }}/{{ CONFIG.name }}:{{ port.vip_port }}"
{%-     endif %}
          }
        }{% if not loop.last %},{% endif %}
{%-   endfor %}
      ],
{%- endif %}
      "privileged": false,
      "parameters": [
        {
          "key": "label",
          "value": "service={{ CONFIG.group }}"
        },
        {
          "key": "label",
          "value": "service_component={{ CONFIG.name }}"
        }
      ],
      "forcePullImage": true
    }
  },
{%- if CONFIG.env is defined %}
  "env": {{ (CONFIG.env | to_nice_json(prefix_indent=2)).strip() }},
{%- endif %}
{%- set health_checks = (CONFIG.ports | default([]) | map(attribute='health_check') | list) + (CONFIG.health_checks | default([])) %}
{%- if health_checks | length > 0 %}
  "healthChecks": [
{%-   for check in health_checks %}
    {
{%-     if check.endpoint is defined %}
      "path": "{{ check.endpoint }}",
      "protocol": "{{ check.type | default('MESOS_HTTP') }}",
      "portIndex": {{ loop.index0 }},
{%-     elif check.command is defined %}
      "protocol": "COMMAND",
      "command": {
        "value": "{{ check.command }}"
      },
{%-     endif %}
      "gracePeriodSeconds": 30,
      "intervalSeconds": 5,
      "timeoutSeconds": 10,
      "maxConsecutiveFailures": 10
    }{% if not loop.last %},{% endif %}
{%-   endfor %}
  ],
{%- endif %}
  "upgradeStrategy": {
    "minimumHealthCapacity": 0.5,
    "maximumOverCapacity": 1
  },
  "labels": {},
{%- if VARS.DOCKER_CREDENTIALS_URI is defined %}
  "fetch": [
    {
      "uri": "{{ VARS.DOCKER_CREDENTIALS_URI }}",
      "extract": true,
      "executable": false,
      "cache": false
    }
  ],
{% endif %}
  "unreachableStrategy": {
    "inactiveAfterSeconds": 30,
    "expungeAfterSeconds": 60
  }
}
'''


class OutputPlugin(OutputPluginBase):

    NAME = 'marathon'
    DESCR = 'Marathon output plugin'
    FILE_EXT = '.json'

    TEMPLATE = _TEMPLATE

    FIELDS = [
        {
            'name': 'name',
            'required': True,
        },
        {
            'name': 'group',
            'required': True,
        },
        {
            'name': 'image',
            'default': '{{ (VARS.DOCKER_IMAGE_PREFIX ~ "/") if VARS.DOCKER_IMAGE_PREFIX is defined else "" }}{{ CONFIG.group }}',
        },
        {
            'name': 'cpus',
            'default': 0.5,
        },
        {
            'name': 'mem',
            'default': 512,
        },
        {
            'name': 'disk',
            'default': 10,
        },
        {
            'name': 'instances',
            'default': 1,
        },
        {
            'name': 'num_azs',
            'default': 3,
        },
        {
            'name': 'ports',
        },
        {
            'name': 'env',
        },
        {
            'name': 'health_checks',
        },
    ]

    def is_needed(self, config):
        # We always (for now) want to output a Marathon config
        return True
