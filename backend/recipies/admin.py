from django.contrib import admin

from .models import IngredientRecipe, Ingredient, Recipe, Tag, TagRecipe


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    verbose_name_plural = 'Ингредиенты'


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    verbose_name_plural = 'Теги'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')
    inlines = (IngredientRecipeInline, TagRecipeInline)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
