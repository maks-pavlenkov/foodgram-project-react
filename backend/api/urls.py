from django.urls import include, path
from rest_framework import routers
from .views import (IngredientViewSet, IsFavoriteViewSet, RecipeViewSet,
                    ShoppingCartViewSet, TagViewSet)


app_name = 'api'
router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('recipes/<int:pk>/favorite/', IsFavoriteViewSet.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view()),
    path('', include(router.urls))
]
