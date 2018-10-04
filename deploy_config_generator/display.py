# This helps make things py3 compatible
from __future__ import print_function


class Display(object):

    _verbosity = 0

    def __init__(self, verbosity):
        self._verbosity = verbosity

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
