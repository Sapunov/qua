from django.contrib import admin

from .models import Categories, Answers, Questions, Keywords, SearchHistory


class AddIdField(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Categories, AddIdField)
admin.site.register(Answers, AddIdField)
admin.site.register(Keywords)


class AnswerInline(admin.StackedInline):
    model = Answers
    readonly_fields = ('version',)
    can_delete = False


class QuestionsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    exclude = ('search_history_clck',)
    inlines= [AnswerInline]


admin.site.register(Questions, QuestionsAdmin)


class SearchHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'query', 'user', 'results',
        'searched_at', 'clicked_at', 'question')


admin.site.register(SearchHistory, SearchHistoryAdmin)
