from django.contrib import admin
from .models import Recipe, Tag, Ingredient, TagRecipe, IngredientRecipe

admin.register(Recipe)
admin.register(Tag)
admin.register(Ingredient)
admin.register(TagRecipe)
admin.register(IngredientRecipe)
