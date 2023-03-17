from django.shortcuts import get_object_or_404
from recipies.models import (FavoriteRecipes, Following, Ingredient, Recipe,
                             ShoppingCart, Tag)
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)
from users.models import User

from .serializers import (IngredientSerializer, IsFavoriteSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          SubscribeSerializer, SubscriptionsSerializer,
                          TagRecipeSerializer)


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(ModelViewSet):
    serializer_class = TagRecipeSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get', )


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    http_method_names = ('get', )


class ShoppingCartViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()

    def perform_create(self, serializer):
        author = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        serializer.save(author=author, recipe=recipe)


class IsFavoriteViewSet(APIView):

    def get_object(self, pk):
        try:
            return FavoriteRecipes.objects.filter(author=self.request.user)
        except Following.DoesNotExist:
            raise status.Http404

    def post(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        request.data['author'] = self.request.user
        request.data['recipe'] = recipe
        serializer = IsFavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(**request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        favorite_recipes = self.get_object(pk).filter(recipe__id=pk)
        favorite_recipes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get_queryset(self):
    #     recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
    #     queryset = FavoriteRecipes.objects.all()
    #     return queryset

    # def perform_create(self, serializer):
    #     author = self.request.user
    #     recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
    #     serializer.save(author=author, recipe=recipe)


class SubscriptionsViewSet(ReadOnlyModelViewSet):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        authors = self.request.user.follower.all()
        print(authors)
        authors_pk = [author.following.pk for author in authors]
        print(authors_pk)
        queryset = User.objects.filter(pk__in=authors_pk)
        print(queryset, 'QUERYSEREEE')
        return queryset


class SubscribeViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Following.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        following = User.objects.get(id=self.kwargs.get('id'))
        serializer.save(user=self.request.user, following=following)
    
    def destroy(self, request, *args, **kwargs):    
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Subscribe(APIView):

    def get_object(self, pk):
        try:
            return Following.objects.get(following=pk)[-1]
        except Following.DoesNotExist:
            raise status.Http404

    def post(self, request, pk):
        following = User.objects.get(id=pk)
        request.data['user'] = self.request.user
        request.data['following'] = following
        serializer = SubscribeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(**request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        following = self.get_object(pk)
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)