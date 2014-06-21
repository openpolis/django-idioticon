import sys
from xml.etree.ElementTree import Element
from django.core.exceptions import ImproperlyConfigured


PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    unicode = str
else:
    string_types = basestring,

# Setup default configurations
IDIOTICON_DEFAULTS = {
    'TEXT_FIELD': 'django.db.models.TextField',
    'KEY_LENGTH': 255,
    'TITLE_LENGTH': 255,
    'CACHE': 'default',
    'CACHE_KEY_PREFIX': 'term-',
    'THEME': 'plain',
    'CONTEXT_LOADER': '',
}

class Theme(object):

    icon = None
    symbol = ''
    wrapper = 'span'

    def render(self, symbol=None, wrapper=None, icon=None):
        wrapper = self.wrapper if wrapper is None else wrapper
        if isinstance(wrapper, string_types):
            wrapper = Element(wrapper)
        symbol = self.symbol if symbol is None else symbol
        if symbol:
            wrapper.text = symbol
        icon = self.icon if icon is None else icon
        if icon:
            wrapper.append(icon)
        return unicode(wrapper)


# plain theme configuration (default)
IDIOTICON_PLAIN = {
    'ICON_TAG': 'abbr',
    'ICON_CLASS': '',
    'SYMBOL': '*',
}

# bootstrap theme configuration
IDIOTICON_BOOTSTRAP = {
    'ICON_TAG': 'span',
    'ICON_CLASS': 'fa fa-fw fa-question-circle',
    'SYMBOL': '',
}

# all themes
THEMES = {
    'plain': IDIOTICON_PLAIN,
    'bootstrap': IDIOTICON_BOOTSTRAP,
}

def get_config(values):

    config = IDIOTICON_DEFAULTS.copy()

    # Merge defaults with settings
    config.update(values)

    # Check the theme
    try:
        theme = values['THEME']
        config['THEME'] = THEMES[values['THEME']].copy()
        config['THEME']['NAME'] = theme
    except KeyError:
        raise ImproperlyConfigured("The IDIOTICON theme is not valid: %s" % values['THEME'])

    return config
