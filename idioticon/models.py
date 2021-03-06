# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from idioticon.conf import settings

try:
    # Deprecated in Django 1.7
    from django.utils.module_loading import import_by_path as import_string

except ImportError:
    # For Django 1.7
    from django.utils.module_loading import import_string

# Definition Field type
TermDefinitionField = import_string(settings.IDIOTICON_TEXT_FIELD) if settings.IDIOTICON_TEXT_FIELD else models.TextField

class TermManager(models.Manager):

    def get_term(self, key, soft_error=False):
        """This method tries to return a term by key.
        Can raise Term.DoesNotExist if soft_error is False (as in default).

        :param key: term
        :type key: str
        :returns: then matching Term
        :rtype Term:
        :raises Term.DoesNotExist
        """
        if isinstance(key, Term):
            return key

        try:
            # use select_related to load main term and requested alias with one query.
            term = self.get_queryset().select_related('main_term').get(key=key)

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
        term = self.get_term(term)
        if not isinstance(alias, Term):
            return self.get_queryset().create(
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
    definition = TermDefinitionField(_("Definition"), blank=True, help_text=_("The definition of the term"))

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
        return self.get_name()

    @property
    def is_main_term(self):
        return self.main_term is None

    @property
    def is_alias(self):
        return not self.is_main_term

    class Meta:
        verbose_name = _("Term")
        verbose_name_plural = _("Terms")

