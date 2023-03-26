from django.urls import include, path
from rest_framework import routers

from .views import (Subscribe, SubscriptionsViewSet, UserViewSet,
                    change_password, token_login, token_logout)


app_name = 'users'
router = routers.DefaultRouter()
router.register(
    'users/subscriptions',
    SubscriptionsViewSet,
    basename='subscriptions'
)
router.register('users', UserViewSet,  basename='user')

urlpatterns = [
    path('auth/token/login/', token_login, name='token_login'),
    path('auth/token/logout/', token_logout, name='token_logout'),
    path('users/set_password/', change_password, name='token_logout'),
    path('users/<int:pk>/subscribe/', Subscribe.as_view()),
    path('', include(router.urls))
]
