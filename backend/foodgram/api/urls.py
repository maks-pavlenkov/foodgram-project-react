from django.urls import include, path
from rest_framework import routers
from .views import RecipeViewSet, TagViewSet, IngredientViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('recipe', RecipeViewSet, basename='recipe')
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]
