"""
Django-idioticon is a module that allows to disseminate html templates with clickable question marks (idioticons).
"""
import logging


__author__ = 'openpolis'
__version__ = (0, 0, 1)

def get_version(version=None):
    """
    Returns a string version number from __version__

    @see PEP 386-compliant
    """
    return ".".join(map(str, __version__))

# Setup default logging.
log = logging.getLogger('idioticon')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)


from idioticon.shortcuts import get_term, add_term, update_term, set_term, delete_term, add_alias
