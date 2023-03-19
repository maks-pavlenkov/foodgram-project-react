from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from recipies.models import (FavoriteRecipes, Following, Ingredient, Recipe,
                             ShoppingCart, Tag, IngredientRecipe)
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import status
from rest_framework import permissions
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
from .permissions import RecipeFavShopFollowPermission



class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (RecipeFavShopFollowPermission,)
    filter_backends = (DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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
    # serializer_class = ShoppingCartSerializer
    # queryset = ShoppingCart.objects.all()

    # def perform_create(self, serializer):
    #     author = self.request.user
    #     recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
    #     serializer.save(author=author, recipe=recipe)

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
    permission_classes = [RecipeFavShopFollowPermission]
    filter_backends = (DjangoFilterBackend,)

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
    permission_classes = [RecipeFavShopFollowPermission]
    filter_backends = (DjangoFilterBackend,)

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
    permission_classes = [RecipeFavShopFollowPermission]
    filter_backends = (DjangoFilterBackend,)

    def get_object(self, pk):
        try:
            return Following.objects.get(following=pk)
        except Following.DoesNotExist:
            return Response('Object not found', status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            following = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response('Object not found', status.HTTP_404_NOT_FOUND)
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