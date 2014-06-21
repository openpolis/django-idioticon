================
django-idioticon
================

.. image:: https://badge.fury.io/py/django-idioticon.png
    :target: https://badge.fury.io/py/django-idioticon

.. image:: https://travis-ci.org/openpolis/django-idioticon.png?branch=master
    :target: https://travis-ci.org/openpolis/django-idioticon

.. image:: https://coveralls.io/repos/openpolis/django-idioticon/badge.png?branch=master
    :target: https://coveralls.io/r/openpolis/django-idioticon?branch=master

Idioticon is a module that allows to disseminate html templates with clickable question marks (idioticons)

Documentation
-------------

The full documentation is at https://django-idioticon.readthedocs.org.

Quickstart
----------

Install django-idioticon::

    pip install django-idioticon


Add ``idioticon`` to ``settings.INSTALLED_APPS`` and execute `syncdb` to create Term table::

    >>> import idioticon
    >>> idioticon.get_term(key='not-existing-term', soft_error=True)
    None

    >>> term = idioticon.add_term('my-term', 'My term')
    >>> idioticon.add_term('my-term', 'My term')
    False

    >>> idioticon.set_term('my-term', 'My new term').name
    'My new term'

    >>> idioticon.update_term('my-term', 'My term').name
    'My term'
    >>> idioticon.update_term('not-existing-term', 'My term')
    False

    >>> idioticon.delete_term('my-term').name
    'My term'

    >>> alias = idioticon.add_alias('my-term', 'my-alias', 'My alias', 'description')
    >>> alias.main_term == idioticon.get_term('my-term')
    True

Features
--------

* Term aliases
* Idioticon administration
* Shortcuts ( get_term, )
* Tests for Django >= 1.5 and Python >= 2.6
* django-modeltranslation integration for multi language site
* Configurable definition field


Settings
--------

Option | Description
-------|------------
IDIOTICON_THEME = 'span' | {% term_tag .. %} loads idioticon/term_THEME.html
IDIOTICON_TEXT_FIELD = '' | Override the default TextField with your custom one.

Template tags
-------------
::

    {% load idioticon %}
    {% term_tag 'my-term' %}

    {% load_terms 'my-term' as term %}
    {{ term.get_name %}
    {{ term.get_definition %}

