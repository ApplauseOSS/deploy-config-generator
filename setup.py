from __future__ import print_function

from setuptools import setup
from setuptools.command.upload import upload
from distutils.cmd import Command

import os
import sys
import subprocess


class ReleaseToPyPICommand(upload):

    def finalize_options(self):
        self.repository = os.environ['PYPI_URL']
        self.username = os.environ['PYPI_USERNAME']
        self.password = os.environ['PYPI_PASSWORD']


class IntegrationTests(Command):
    description = "Command to run integration tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tests_basedir = os.path.join(os.path.dirname(__file__), 'tests', 'integration')
        print('Running integration tests in %s' % tests_basedir)
        tests = []
        for entry in sorted(os.listdir(tests_basedir)):
            if not os.path.isdir(os.path.join(tests_basedir, entry)):
                continue
            tests.append(entry)
        for test in tests:
            print()
            print('Starting integration test: %s' % test)
            test_basedir = os.path.join(tests_basedir, test)
            runme_path = os.path.join(test_basedir, 'runme.sh')
            if not os.path.exists(runme_path):
                print('SKIPPED...could not find runme.sh script')
                continue
            try:
                print('Running %s' % runme_path)
                # This allows the output to make sense in the case of a failure
                sys.stdout.flush()
                retcode = subprocess.call(runme_path)
            except Exception as e:
                print('FAILED with exception: %s' % str(e))
                sys.exit(1)
            if retcode != 0:
                print('FAILED with exit code: %d' % retcode)
                sys.exit(1)
            else:
                print('SUCCESS')


setup(
    name='deploy-config-generator',
    version='1.0.0',
    url='https://github.com/ApplauseOSS/deploy-config-generator',
    license='MIT',
    description='Utility to generate service deploy configurations',
    author='Applause',
    author_email='ops@applause.com',
    test_suite='tests.unit',
    zip_safe=False,
    # Packages are specified manually to prevent the 'tests' dir from being installed
    packages=[
        'deploy_config_generator',
        'deploy_config_generator.output',
    ],
    install_requires=[
        'Jinja2>=2.8',
        'PyYAML',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'deploy-config-generator = deploy_config_generator.__main__:main',
            'app-config = deploy_config_generator.__main__:main',
        ]
    },
    cmdclass={
        'release_to_pypi': ReleaseToPyPICommand,
        'integration': IntegrationTests,
    }
)
