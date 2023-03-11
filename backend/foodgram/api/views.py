from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from recipies.models import Recipe, Tag, Ingredient
from .serializers import RecipeSerializer, TagRecipeSerializer, IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    # queryset = Recipe.objects.all()

    def get_queryset(self):
        queryset = Recipe.objects.all()
        author = self.request.query_params.get('author', None)
        print(author, '09-=0980987890-987654567890-0987675667890-')
        print(queryset[0].author.pk)
        print(queryset.filter(author_username=author))
        if author is not None:
            return queryset.filter(author=author)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagRecipeSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
