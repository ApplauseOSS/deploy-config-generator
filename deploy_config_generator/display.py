# This helps make things py3 compatible
from __future__ import print_function

from six import with_metaclass

from deploy_config_generator.utils import Singleton


class Display(with_metaclass(Singleton, object)):

    _verbosity = 0

    def __init__(self, verbosity=None):
        if verbosity:
            self.set_verbosity(verbosity)

    def set_verbosity(self, verbosity):
        self._verbosity = verbosity

    def get_verbosity(self):
        return self._verbosity

    def display(self, msg='', verbosity_level=0):
        if self._verbosity >= verbosity_level:
            print(msg)

    def v(self, msg=''):
        self.display(msg, 1)

    def vv(self, msg=''):
        self.display(msg, 2)

    def vvv(self, msg=''):
        self.display(msg, 3)

    def vvvv(self, msg=''):
        self.display(msg, 4)
