from django.contrib import admin

from .models import Categories, Answers, Questions, Keywords


class AddIdField(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Categories, AddIdField)
admin.site.register(Answers, AddIdField)
admin.site.register(Questions, AddIdField)
admin.site.register(Keywords)
