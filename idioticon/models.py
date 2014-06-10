# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_term(key, resolve_alias=True, soft_error=True):
    """
    Retrieve a term by key.
    This is a shortcut to use Term.objects (TermManager).

    :param key:
    :type key: Term or str
    :param resolve_alias:
    :type resolve_alias: bool
    :param soft_error:
    :type soft_error: bool
    :return: a required Term or None if soft_error is True and key not found.
    :rtype: Term or bool
    :raises Term.DoesNotExist
    """
    return Term.objects.get_term(key, resolve_alias=resolve_alias, soft_error=soft_error)


def add_term(key, name='', definition=''):
    """
    Add a term if not already exists.

    :param key:
    :type key: Term or str
    :param name:
    :type name: str
    :param definition:
    :type definition: str
    :return: created Term or False
    :rtype: bool or Term
    """
    term, created = Term.objects.get_or_create(key=key, defaults={
        'name': name,
        'definition': definition,
    })
    if not created:
        return False
    return term


def set_term(key, name=None, definition=None):
    """
    Set a term parameters if already exists or add it.

    :param key:
    :type key: Term or str
    :param name: new name
    :type name: str or None
    :param definition: new definition
    :type definition: str or None
    :return: updated or added Term
    :rtype: Term
    """
    term = get_term(key, resolve_alias=False, soft_error=True)
    if term is None:
        term = add_term(key)
    if name is not None:
        term.name = name
    if definition is not None:
        term.definition = definition

    return term


def update_term(key, name=None, definition=None):
    """
    Update a term parameters only if already exists.

    :param key:
    :type key: Term or str
    :param name: new name
    :type name: str or None
    :param definition: new definition
    :type definition: str or None
    :return: updated Term or False
    :rtype: Term or bool
    """
    term = get_term(key, resolve_alias=False, soft_error=True)
    if term is None:
        return False
    if name is not None:
        term.name = name
    if definition is not None:
        term.definition = definition
    term.save()
    return term


def delete_term(key, alias_cascade=True):
    """
    Delete a term with its aliases.

    :param key:
    :type key: Term or str
    :param alias_cascade: Remove all linked aliases
    :type alias_cascade: bool
    :return: deleted Term or False
    :rtype: bool or Term
    """
    term = get_term(key, resolve_alias=False, soft_error=True)
    if term is None:
        return False

    if alias_cascade:
        for alias in term.aliases.all():
            alias.delete()

    term.delete()

    return term


def add_alias(term, alias, name='', definition=''):
    """
    Adds an alias Term to term.

    :param term: a Term object or key str
    :type term: Term or str
    :param alias: a Term object or key str
    :type alias: Term or str
    :param name: new name
    :type name: str or None
    :param definition: new definition
    :type definition: str or None
    :return: added Alias
    :rtype: Term or bool
    :raises Term.DoesNotExist
    """
    term = get_term(term, resolve_alias=False, soft_error=True)
    if term is None:
        return False
    return Term.objects.add_alias(term, alias, name, definition)


class TermManager(models.Manager):
    def get_term(self, key, resolve_alias=True, soft_error=False):
        """This method tries to return a term by key.
        Automatically load the main term if an alias key is provided.
        Can raise Term.DoesNotExist if soft_error is False (as in default).

        :param key: term
        :type key: str
        :param resolve_alias: default True
        :type resolve_alias: bool
        :param soft_error: default False
        :type soft_error: bool
        :returns: then matching Term
        :rtype Term:
        :raises Term.DoesNotExist
        """
        if isinstance(key, Term):
            return key

        try:
            # use select_related to load main term and requested alias with one query.
            term = self.get_queryset().select_related('main_term').get(key=key)

            if resolve_alias and not term.is_main_term:
                term = term.main_term

        except Term.DoesNotExist:
            if not soft_error:
                raise
            term = None

        return term

    def add_alias(self, term, alias, name='', definition=''):
        """Adds an Alias to main term.

        :param term: Alias main term
        :type term: Term
        :param alias: alias key
        :type alias: str or Term
        :param name: alias name override
        :type name: str
        :param definition: alias definition override
        :type definition: str
        :returns: a Term alias
        :rtype: Term
        """
        if not isinstance(alias, Term):
            return Term.objects.create(
                key=alias,
                name=name,
                definition=definition,
                main_term=term)
        alias.main_term = term
        alias.save()
        return alias

class Term(models.Model):
    """
    An idioticon is a glossary.

    It is used in popovers all over the website, and it may be used to build
    a proper glossary page.

    It is called idioticon, because it's a much more interesting name.
    """
    key = models.SlugField(max_length=255, unique=True,
                           help_text=_("A single word, to use as key in popovers' inclusion tags"))
    name = models.CharField(_("Term"), blank=True, max_length=255, help_text=_("The term"))
    definition = models.TextField(_("Definition"), blank=True, help_text=_("The definition of the term"))

    main_term = models.ForeignKey('self', null=True, blank=True, related_name='aliases',
                                  help_text=_("Main definition"))

    objects = TermManager()

    def get_name(self):
        if self.name:
            return self.name
        if self.is_alias:
            return self.main_term.get_name()
        return self.key

    def get_definition(self):
        if self.definition:
            return self.definition
        if self.is_alias:
            return self.main_term.get_definition()
        return ''

    def add_alias(self, key, name='', description=''):
        return self.objects.add_alias(self, key, name, description)

    def __unicode__(self):
        return self.name

    @property
    def is_main_term(self):
        return self.main_term is None

    @property
    def is_alias(self):
        return not self.is_main_term

    class Meta:
        verbose_name = _("Term")
        verbose_name_plural = _("Terms")

