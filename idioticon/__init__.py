import logging


__author__ = 'openpolis'
__version__ = (0, 0, 1)


# Setup default logging.
log = logging.getLogger('idioticon')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)


from .models import get_term
