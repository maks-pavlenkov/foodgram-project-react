from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')


admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
