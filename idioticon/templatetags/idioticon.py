from __future__ import absolute_import
from django import template
from django.conf import settings
from django.template import (Node, TemplateSyntaxError, Context)
from django.template.loader import get_template
from idioticon import shortcuts


register = template.Library()

class LoadTermsNode(Node):
    def __init__(self, variables, terms):
        self.variables = variables
        self.terms = terms

    def render(self, context):
        for variable, term in zip(self.variables, self.terms):
            context[variable] = shortcuts.get_term(term)
        return ''


@register.simple_tag(name="term_tag")
def do_term_tag(term_key, **kwargs):

    theme = kwargs.pop('theme', settings.IDIOTICON_THEME)

    context = Context()
    context.update(kwargs)

    try:
        context['term'] = shortcuts.get_term(term_key)
        template_name = 'idioticon/term_%s.html' % theme
        template = get_template(template_name)
        return template.render(context)
    except:
        if settings.TEMPLATE_DEBUG:
            raise
        return ''


@register.tag("load_terms")
def do_load_terms(parser, token):
    """
    This will store a list of terms in the context.

    Usage::

        {% load_terms 'my-term' 'other-term' as my_term other_term %}
        {{ my_term.get_title }}: {{ my_term.get_definition }}

    """
    # token.split_contents() isn't useful here because this tag doesn't accept variable as arguments
    args = token.contents.split()

    try:
        as_index = args.index('as')
    except ValueError:
        raise TemplateSyntaxError("'load_terms' requires '*terms as *variable' (got %r)" % args)

    names, terms = args[as_index+1:], args[1:as_index]

    if len(names) != len(terms):
        raise TemplateSyntaxError("'load_terms' requires '*terms as *variable' (got %r)" % args)
    return LoadTermsNode(names, terms)