from setuptools import setup
from setuptools.command.upload import upload

import os


class UploadToInternalRepoCommand(upload):
    def finalize_options(self):
        self.repository = os.environ.get('APPLAUSE_REPO_URL', 'https://repo.applause.com/repository/pypi-internal/')
        self.username = os.environ['APPLAUSE_REPO_USER_NAME']
        self.password = os.environ['APPLAUSE_REPO_PASSWORD']


setup(
    name='applause-deploy-config-generator',
    version='0.1.0',
    url='https://github.com/ApplauseAQI/applause-deploy-config-generator',
    license='Applause',
    description='Utility to generate service deploy configurations',
    author='Applause',
    author_email='ops@applause.com',
    test_suite='tests',
    zip_safe=False,
    # Packages are specified manually to prevent the 'tests' dir from being installed
    packages=[
        'deploy_config_generator',
        'deploy_config_generator.output',
    ],
    install_requires=[
        'Jinja2>=2.7',
        'PyYAML',
        'six',
    ],
    entry_points={
        'console_scripts': [
            # Blame Andrew's lack of imagination
            'applause-deploy-config-generator = deploy_config_generator.__main__:main',
            # Blame Chris
            'dcos-confabulator = deploy_config_generator.__main__:main',
            # Blame Jason
            'dcos-wombat = deploy_config_generator.__main__:main',
        ]
    },
    cmdclass={
        'upload_to_nexus': UploadToInternalRepoCommand
    }
)
