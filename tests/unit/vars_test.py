import inspect
import six
import unittest

# py2/3 compatibility
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from deploy_config_generator.vars import Vars, VarsParser
from deploy_config_generator.errors import VarsParseError


class TestVars (unittest.TestCase):

    def setUp(self):
        # Map PY3 name for function (used in code below) to PY2 name
        # This allows us to run the tests on both without deprecation warnings
        if six.PY2:
            self.assertRaisesRegex = self.assertRaisesRegexp

    def wrap_file(self, data):
        return StringIO(inspect.cleandoc(data))

    def vars_parse(self, data, varset):
        VarsParser(fh=self.wrap_file(data), varset=varset).parse()

    def test_read_vars_simple(self):
        vars_content = '''
        FOO=bar
        BAR=baz
        '''
        my_vars = Vars()
        self.vars_parse(vars_content, my_vars)

        self.assertEqual(dict(my_vars), { 'FOO': 'bar', 'BAR': 'baz' })

    def test_read_vars_comment(self):
        vars_content = '''
        # Some comment
        FOO=bar
        BAR=baz # Another comment
        '''
        my_vars = Vars()
        self.vars_parse(vars_content, my_vars)

        self.assertEqual(dict(my_vars), { 'FOO': 'bar', 'BAR': 'baz' })

    def test_read_vars_empty_lines(self):
        vars_content = '''

        FOO=bar

        BAR=baz

        '''
        my_vars = Vars()
        self.vars_parse(vars_content, my_vars)

        self.assertEqual(dict(my_vars), { 'FOO': 'bar', 'BAR': 'baz' })

    def test_read_vars_quotes(self):
        vars_content = '''
        SOME_VAR="foo"bar
        ANOTHER_VAR="foo 'bar' baz"
        '''
        my_vars = Vars()
        self.vars_parse(vars_content, my_vars)

        self.assertEqual(dict(my_vars), { 'SOME_VAR': 'foobar', 'ANOTHER_VAR': "foo 'bar' baz" })

    def test_read_vars_other(self):
        vars_content = '''
        TEST=foo=bar
        TEST1=foo1 TEST2=foo2
        '''
        my_vars = Vars()
        self.vars_parse(vars_content, my_vars)

        self.assertEqual(dict(my_vars), { 'TEST': 'foo=bar', 'TEST1': 'foo1', 'TEST2': 'foo2' })

    def test_var_quoting(self):
        vars_content = r'''
        SOME_VAR="[{\"name\":\"foo\",\"id\":\"bar\"}]"
        ANOTHER_VAR='foo \"bar\" baz'
        '''
        my_vars = Vars()
        self.vars_parse(vars_content, my_vars)

        self.assertEqual(dict(my_vars), { 'SOME_VAR': '[{"name":"foo","id":"bar"}]', 'ANOTHER_VAR': r'foo \"bar\" baz' })

    def test_var_replacement(self):
        vars_content = '''
        FOO=bar
        BAR=$FOO
        BAZ=${BAR}
        SOME_VAR="foo ${FOO} $BAR baz"
        ANOTHER_VAR="foo ${FOO baz"
        YET_ANOTHER_VAR='foo $BAR ${BAR} baz'
        '''
        my_vars = Vars()
        self.vars_parse(vars_content, my_vars)

        self.assertEqual(
            dict(my_vars),
            { 'FOO': 'bar', 'BAR': 'bar', 'BAZ': 'bar', 'SOME_VAR': 'foo bar bar baz', 'ANOTHER_VAR': 'foo ${FOO baz', 'YET_ANOTHER_VAR': 'foo $BAR ${BAR} baz' }
        )

    def test_var_replacement_between_files(self):
        vars_content1 = '''
        FOO=bar
        '''
        vars_content2 = '''
        BAR=$FOO
        '''
        my_vars = Vars()
        self.vars_parse(vars_content1, my_vars)
        self.vars_parse(vars_content2, my_vars)

        self.assertEqual(dict(my_vars), { 'FOO': 'bar', 'BAR': 'bar' })

    def test_parse_errors_1(self):
        vars_content = '''
        FOO=bar baz
        '''
        my_vars = Vars()
        with self.assertRaisesRegex(VarsParseError, "line 1: Did not find expected token '=' after var name"):
            self.vars_parse(vars_content, my_vars)

    def test_parse_errors_2(self):
        vars_content = '''
        FOO="bar
        '''
        my_vars = Vars()
        with self.assertRaisesRegex(VarsParseError, 'line 1: Did not find expected closing quote `"`'):
            self.vars_parse(vars_content, my_vars)

    def test_parse_errors_3(self):
        vars_content = '''
        =bar
        '''
        my_vars = Vars()
        with self.assertRaisesRegex(VarsParseError, "line 1: Encountered '=' before var name"):
            self.vars_parse(vars_content, my_vars)

    def test_parse_errors_4(self):
        vars_content = '''
        FOO BAR=baz
        '''
        my_vars = Vars()
        with self.assertRaisesRegex(VarsParseError, "line 1: Did not find expected token '=' after var name"):
            self.vars_parse(vars_content, my_vars)

    def test_parse_errors_5(self):
        vars_content = '''
        FOO= bar
        '''
        my_vars = Vars()
        with self.assertRaisesRegex(VarsParseError, "line 1: Did not find expected token '=' after var name"):
            self.vars_parse(vars_content, my_vars)
