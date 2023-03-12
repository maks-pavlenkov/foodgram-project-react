from django.urls import include, path
from rest_framework import routers
from .views import RecipeViewSet, TagViewSet, IngredientViewSet, ShoppingCartViewSet, IsFavoriteViewSet, SubscriptionsViewSet, SubscribeViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register(
    r'recipes/(?P<id>\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shopping_cart'
)
router.register(
    r'recipes/(?P<id>\d+)/favorite',
    IsFavoriteViewSet,
    basename='favorite'
)
router.register(
    'users/subscriptions',
    SubscriptionsViewSet,
    basename='subscriptions'
)
router.register(
    r'users/(?P<id>\d+)/subscribe',
    SubscribeViewSet,
    basename='subscribe'
)

urlpatterns = [
    path('v1/', include(router.urls))
]
