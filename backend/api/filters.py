from django_filters import FilterSet
from django_filters.rest_framework import filters

from recipies.models import Recipe
from users.models import User


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    def get_is_favorited(self, queryset, name, value):
        instance = self.request.user.favorites
        favs_pk = [pk[0] for pk in instance.values_list('pk')]
        recipes = []
        for i in favs_pk:
            recipes.append(instance.get(id=i).recipe.id)
        if self.request.user.is_authenticated and value:
            return queryset.filter(
                pk__in=recipes
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        instance = self.request.user.shoppingcart
        shop_cart = [pk[0] for pk in instance.values_list('pk')]
        recipes = []
        for i in shop_cart:
            recipes.append(instance.get(id=i).recipe.id)
        if self.request.user.is_authenticated and value:
            return queryset.filter(
                pk__in=recipes
                )
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
