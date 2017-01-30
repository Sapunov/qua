from django.contrib import admin

from .models import Answer, Question, Keyword, SearchHistory, ExternalResource


class AddIdField(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Answer, AddIdField)
admin.site.register(Keyword)


class AnswerInline(admin.StackedInline):
    model = Answer
    readonly_fields = ('version',)
    can_delete = False


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    exclude = ('search_history_clck',)
    inlines= [AnswerInline]


admin.site.register(Question, QuestionAdmin)


class SearchHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'query', 'user', 'results',
        'searched_at', 'clicked_at', 'question', 'external',
        'external_resource'
    )


admin.site.register(SearchHistory, SearchHistoryAdmin)

admin.site.register(ExternalResource)
