from django.contrib import admin

from api import models


class AddIdField(admin.ModelAdmin):

    readonly_fields = ('id',)


admin.site.register(models.Answer, AddIdField)
admin.site.register(models.Keyword)


class AnswerInline(admin.StackedInline):

    model = models.Answer
    readonly_fields = ('version',)
    can_delete = False


class QuestionAdmin(admin.ModelAdmin):

    readonly_fields = ('id',)
    exclude = ('search_history_clck',)
    inlines = [AnswerInline]


admin.site.register(models.Question, QuestionAdmin)


class SearchHistoryAdmin(admin.ModelAdmin):

    readonly_fields = (
        'id', 'query', 'user', 'results',
        'searched_at', 'clicked_at', 'question', 'external',
        'external_resource'
    )

class ExternalResourceAdmin(admin.ModelAdmin):

    readonly_fields = (
        'id', 'scheme', 'hostname', 'update_interval',
        'se_id', 'created_at', 'updated_at', '_content_hash'
    )
    exclude = ('created_by', 'updated_by', '_url')


admin.site.register(models.SearchHistory, SearchHistoryAdmin)

admin.site.register(models.ExternalResource, ExternalResourceAdmin)
