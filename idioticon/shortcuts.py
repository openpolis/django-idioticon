

def get_term_model():
    from idioticon.models import Term
    return Term


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
    return get_term_model().objects.get_term(key, soft_error=soft_error)


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
    term, created = get_term_model().objects.get_or_create(key=key, defaults={
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
    term = get_term(key, soft_error=True)
    if term is None:
        term = add_term(key)
    if name is not None:
        term.name = name
    if definition is not None:
        term.definition = definition
    term.save()
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
    term = get_term(key, soft_error=True)
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
    term = get_term(key, soft_error=True)
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
    term = get_term(term, soft_error=True)
    if term is None:
        return False
    return get_term_model().objects.add_alias(term, alias, name, definition)