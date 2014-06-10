"""
Django-idioticon is a module that allows to disseminate html templates with clickable question marks (idioticons).
"""
import logging


__author__ = 'openpolis'
__version__ = (0, 0, 1)

def get_version(version=None):
    "Returns a PEP 386-compliant version number from VERSION."

    return ".".join(map(str, __version__))


def setup():
    """
    Configure the settings (this happens as a side effect of accessing the
    first setting), configure logging and populate the app registry.
    """
    from django.apps import apps
    from django.conf import settings
    from django.utils.log import configure_logging

    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
    apps.populate(settings.INSTALLED_APPS)

# Setup default logging.
log = logging.getLogger('idioticon')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)


from idioticon.shortcuts import get_term, add_term, update_term, set_term, delete_term, add_alias
