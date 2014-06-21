from modeltranslation.translator import translator, TranslationOptions
from idioticon.models import Term

class TermTranslationOptions(TranslationOptions):
    fields = ('name', 'definition',)

translator.register(Term, TermTranslationOptions)