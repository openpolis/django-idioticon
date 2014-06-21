from django.conf import settings

TEXT_FIELD = getattr(settings, 'IDIOTICON_TEXT_FIELD', '')
THEME = getattr(settings, 'IDIOTICON_THEME', 'span')

setattr(settings, 'IDIOTICON_TEXT_FIELD', TEXT_FIELD)
setattr(settings, 'IDIOTICON_THEME', THEME)

