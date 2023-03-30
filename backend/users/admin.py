from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy
from .models import User
from recipies.models import ShoppingCart


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    inlines = (ShoppingCartInline,)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
