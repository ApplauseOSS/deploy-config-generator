import inspect
import unittest

from deploy_config_generator.template import Template


class TestTemplate (unittest.TestCase):

    def setUp(self):
        self._template = Template()

    def test_template_plain(self):
        tpl = '''
        Plain text
        More text
        '''
        output = self._template.render_template(inspect.cleandoc(tpl), {})

        self.assertEqual(output, 'Plain text\nMore text')

    def test_template_var_simple(self):
        tpl = '''
        foo {{ bar }} baz
        '''
        my_vars = { 'bar': 'whatever' }
        output = self._template.render_template(inspect.cleandoc(tpl), my_vars)

        self.assertEqual(output, 'foo whatever baz')

    def test_template_if_statement(self):
        tpl = '''
        foo
        {% if bar is defined %}
        bar
        {% endif %}
        baz
        '''
        output = self._template.render_template(inspect.cleandoc(tpl), {})

        self.assertEqual(output, 'foo\n\nbaz')

    def test_template_filter_to_json(self):
        tpl = '''
        {{ foo | to_json }}
        '''
        my_vars = { 'foo': { 'bar': ['item 1', 'item 2'] } }
        output = self._template.render_template(inspect.cleandoc(tpl), my_vars)

        self.assertEqual(output, '{"bar": ["item 1", "item 2"]}')
