================
django-idioticon
================

.. image:: https://badge.fury.io/py/idioticon.png
    :target: https://badge.fury.io/py/idioticon

.. image:: https://travis-ci.org/joke2k/idioticon.png?branch=master
    :target: https://travis-ci.org/joke2k/idioticon

.. image:: https://coveralls.io/repos/joke2k/idioticon/badge.png?branch=master
    :target: https://coveralls.io/r/joke2k/idioticon?branch=master

Idioticon is a module that allows to disseminate html templates with clickable question marks (idioticons)

Documentation
-------------

The full documentation is at https://idioticon.readthedocs.org.

Quickstart
----------

Install django-idioticon::

    pip install idioticon

Then use it in a project::

    >>> import idioticon
    >>> idioticon.get_term(key='not-existing-term', soft_error=False)
    False


Features
--------

* Term aliases
* Idioticon administration
* Shortcuts ( get_term, )
* Tests
