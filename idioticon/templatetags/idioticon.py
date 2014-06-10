from __future__ import absolute_import
from django import template
from idioticon import log
from idioticon import shortcuts

register = template.Library()

@register.inclusion_tag('idioticon/term_icon.html')
def term(term_key, **kwargs):

    # get the term context
    context = {}
    context.update(kwargs)
    context['term'] = shortcuts.get_term(term_key)
    log.info('TAG for term: %s' % context['term'])

    return context