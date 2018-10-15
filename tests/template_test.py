import inspect
import unittest

from deploy_config_generator.template import render_template


class TestTemplate (unittest.TestCase):

    def test_template_plain(self):
        tpl = '''
        Plain text
        More text
        '''
        output = render_template(inspect.cleandoc(tpl), {})

        self.assertEqual(output, 'Plain text\nMore text')

    def test_template_var_simple(self):
        tpl = '''
        foo {{ bar }} baz
        '''
        my_vars = { 'bar': 'whatever' }
        output = render_template(inspect.cleandoc(tpl), my_vars)

        self.assertEqual(output, 'foo whatever baz')

    def test_template_if_statement(self):
        tpl = '''
        foo
        {% if bar is defined %}
        bar
        {% endif %}
        baz
        '''
        output = render_template(inspect.cleandoc(tpl), {})

        self.assertEqual(output, 'foo\n\nbaz')

    def test_template_filter_to_json(self):
        tpl = '''
        {{ foo | to_json }}
        '''
        my_vars = { 'foo': { 'bar': ['item 1', 'item 2'] } }
        output = render_template(inspect.cleandoc(tpl), my_vars)

        self.assertEqual(output, '{"bar": ["item 1", "item 2"]}')
