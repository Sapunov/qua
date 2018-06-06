from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserSession


class TokenAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'access_token', 'user', 'created',
        'browser_full', 'os_full', 'ip_address', 'last_use')
    fields = (
        'id', 'access_token', 'user', 'user_agent',
        'ip_address', 'last_use', 'created',
        'browser', 'browser_version', 'os', 'os_version')
    readonly_fields = ('id', 'created', 'last_use')
    ordering = ('-id',)


admin.site.register(UserSession, TokenAdmin)
admin.site.register(User, UserAdmin)
