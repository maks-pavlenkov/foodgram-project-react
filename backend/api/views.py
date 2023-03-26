from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import RecipeFilter
from .permissions import RecipeFavShopFollowPermission
from .serializers import (IngredientSerializer, IsFavoriteSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagRecipeSerializer)
from recipies.models import (FavoriteRecipes, Following, Ingredient,
                             IngredientRecipe, Recipe, ShoppingCart, Tag)


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (RecipeFavShopFollowPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        shop_cart = get_object_or_404(ShoppingCart, user=request.user)
        ingredients = IngredientRecipe.objects.filter(
            recipe__in=shop_cart.recipes.all()
        ).values(
            'ingredient__name', 'ingredient__units'
        ).order_by(
            'ingredient__name'
        ).annotate(
            ingredient_total=Sum('amount')
        )
        draw = []
        for ingr in ingredients:
            draw.append(
                f'{ingr["ingredient__name"]} '
                f'({ingr["ingredient__units"]})'
                f' - {ingr["ingredient_total"]} \n'
            )
        resp = HttpResponse(draw, content_type='text/plain; charset=UTF-8')
        resp['Content-Disposition'] = (
            'attachment; filename={0}'.format('shopping_cart.txt')
        )
        return resp


class TagViewSet(ModelViewSet):
    serializer_class = TagRecipeSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    http_method_names = ('get',)
    permission_classes = (permissions.AllowAny,)
    pagination_class = None

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            return queryset.filter(name__icontains=name)
        return queryset


class ShoppingCartViewSet(APIView):
    permission_classes = [RecipeFavShopFollowPermission]
    filter_backends = (DjangoFilterBackend,)

    def get_object(self, pk):
        try:
            return ShoppingCart.objects.filter(author=self.request.user)
        except ShoppingCart.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def post(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        request.data['author'] = self.request.user
        request.data['recipe'] = recipe
        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(**request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shop_cart = self.get_object(pk=pk).filter(recipe__pk=pk)
        shop_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IsFavoriteViewSet(APIView):
    permission_classes = [RecipeFavShopFollowPermission]
    filter_backends = (DjangoFilterBackend,)

    def get_object(self, pk):
        try:
            return FavoriteRecipes.objects.filter(author=self.request.user)
        except Following.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

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
