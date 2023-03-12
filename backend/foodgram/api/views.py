from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from django.shortcuts import get_object_or_404
from recipies.models import Recipe, Tag, Ingredient, ShoppingCart, FavoriteRecipes, Following
from users.models import User
from .serializers import RecipeSerializer, TagRecipeSerializer, IngredientSerializer, ShoppingCartSerializer, IsFavoriteSerializer, SubscriptionsSerializer, SubscribeSerializer


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    # def get_queryset(self):
    #     queryset = Recipe.objects.all()
    #     req_author = self.request.query_params.get('author', None)
    #     author = get_object_or_404(User, username=req_author)
    #     if author is not None:
    #         return queryset.filter(author=author)
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(ModelViewSet):
    serializer_class = TagRecipeSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class ShoppingCartViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        queryset = ShoppingCart.objects.all()
        return queryset
    
    def perform_create(self, serializer):
        author = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        print(self.request.user)
        print(self.kwargs)
        serializer.save(author=author, recipe=recipe)

class IsFavoriteViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = IsFavoriteSerializer

    def get_queryset(self):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        queryset = FavoriteRecipes.objects.all()
        return queryset
    
    def perform_create(self, serializer):
        author = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        serializer.save(author=author, recipe=recipe)


class SubscriptionsViewSet(ReadOnlyModelViewSet):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        user_id = self.request.user.pk
        queryset = User.objects.filter(id=user_id)
        print(queryset, 'QUERYSEREEE')
        return queryset

class SubscribeViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Following.objects.filter(user=user)
        return queryset
    
    def perform_create(self, serializer):
        print(self.kwargs)
        print(self.request.data)
        following = User.objects.get(id=self.kwargs.get('id'))
        serializer.save(user=self.request.user, following=following)