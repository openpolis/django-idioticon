from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Term

class TermTypeFilter(SimpleListFilter):
    title = 'Type of term'
    parameter_name = 'term_type'

    def lookups(self, request, model_admin):
        return (
            ('main', 'Main term'),
            ('linked', 'Linked term'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'main':
            return queryset.filter(main_term__isnull=True)
        elif self.value() == 'linked':
            return queryset.filter(main_term__isnull=False)

class TermInline(admin.TabularInline):
    model = Term
    extra = 1
    fields = ('key', 'name')

class TermAdmin(admin.ModelAdmin):
    prepopulated_fields = {"key": ("name",)}
    list_filter = [TermTypeFilter, ]
    inlines = [TermInline, ]
    ordering = ('key', )
    list_display = ('key', 'name', 'main_term')
    search_fields = ('key', 'name',)

admin.site.register(Term, TermAdmin)