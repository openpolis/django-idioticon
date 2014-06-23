from django.template import Template, Context
from django.test import TestCase
import idioticon
from idioticon.templatetags.idioticon import do_term_tag, do_load_terms


class TestIdioticonTemplateTags(TestCase):

    TEMPLATE = Template("""
{% load idioticon %}
{% load_terms 'foo' 'bar' as foo bar %}
FOO={{ foo.get_name }}
BAR={{ bar.get_name }}""")

    def test_term_tag(self):
        title = 'MyTerm'
        definition = 'My definition'
        idioticon.add_term('my-term', 'MyTerm', 'My definition')

        self.assertIn(title, do_term_tag('my-term'))
        self.assertIn(definition, do_term_tag('my-term'))

    def test_term_tag_for_not_existing_key(self):
        self.assertEqual('', do_term_tag('not-existing-term'))

    def test_load_terms(self):
        self.assertTrue(idioticon.add_term('foo', 'Foo'))
        self.assertTrue(idioticon.add_term('bar', 'Bar'))

        rendered = self.TEMPLATE.render(Context({}))

        self.assertIn('FOO=Foo', rendered)
        self.assertIn('BAR=Bar', rendered)