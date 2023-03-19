from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, IsFavoriteViewSet, RecipeViewSet,
                    ShoppingCartViewSet, Subscribe, SubscribeViewSet,
                    SubscriptionsViewSet, TagViewSet)
from users.views import UserViewSet, change_password, token_login, token_logout

app_name = 'api'

router = routers.DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet, basename='ingredients')
# router.register(
#     r'recipes/(?P<id>\d+)/shopping_cart',
#     ShoppingCartViewSet,
#     basename='shopping_cart'
# )
router.register(
    'users/subscriptions',
    SubscriptionsViewSet,
    basename='subscriptions'
)
router.register('users', UserViewSet,  basename='users')
# router.register(
#     r'recipes/(?P<id>\d+)/favorite',
#     IsFavoriteViewSet,
#     basename='favorite'
# )
# router.register(
#     'users/subscriptions',
#     SubscriptionsViewSet,
#     basename='subscriptions'
# )
# router.register(
#     r'users/(?P<id>\d+)/subscribe',
#     SubscribeViewSet,
#     basename='subscribe'
# )
# print(router.urls)

urlpatterns = [
    path('auth/token/login/', token_login, name='token_login'),
    path('auth/token/logout/', token_logout, name='token_logout'),
    path('users/set_password/', change_password, name='token_logout'),
    path('users/<int:pk>/subscribe/', Subscribe.as_view()),
    path('recipes/<int:pk>/favorite/', IsFavoriteViewSet.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view()),
    path('', include(router.urls))
]
print(router.urls)
