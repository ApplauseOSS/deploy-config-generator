import subprocess

from deploy_config_generator.utils import yaml_load

SOPS_BINARY = 'sops'


class SecretsException(Exception):

    def __init__(self, path, stderr):
        self.path = path
        self.stderr = stderr
        super().__init__('Failed to decrypt secrets')


class Secrets(dict):

    '''
    This class manages a set of SOPS-encrypted secrets
    '''

    def load_secrets_file(self, path):
        cp = subprocess.run([SOPS_BINARY, 'decrypt', '--output-type=yaml', path], capture_output=True)
        if cp.returncode != 0:
            raise SecretsException(path, cp.stderr)
        # Parse decrypted YAML from SOPS
        data = yaml_load(cp.stdout)
        self.update(data)
