from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipies.models import (FavoriteRecipes, Ingredient,
                             IngredientRecipe, Recipe, ShoppingCart, Tag,
                             TagRecipe)
from users.serializers import UserSerializer
from foodgram.settings import SMALL_INT_NUMBER
from .fields import Base64ImageField


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(
        required=True
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')

    def validate_amount(self, attrs):
        if attrs > SMALL_INT_NUMBER:
            raise serializers.ValidationError('Число должно быть меньше 32767')
        return super().validate(attrs)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tag

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.name
        representation['color'] = instance.color
        representation['slug'] = instance.slug

        return representation


class TagRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all()
    )

    class Meta:
        fields = ('id',)
        model = TagRecipe

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.name
        representation['color'] = instance.color
        representation['slug'] = instance.slug

        return representation


class AmountToIngrSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagRecipeSerializer(many=True, required=False)
    ingredients = AmountToIngrSerializer(
        many=True,
        read_only=True,
        source='amounts'
    )
    is_favorite = serializers.SerializerMethodField('get_is_favorite')
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorite(self, obj):
        try:
            if self.context['request'].user.is_anonymous:
                return False
            user = self.context['request'].user
            return user.favorites.filter(recipe_id=obj.pk).exists()
        except Exception:
            return False

    def get_is_in_shopping_cart(self, obj):
        try:
            if self.context['request'].user.is_anonymous:
                return False
            user = self.context['request'].user
            return user.shoppingcart.filter(recipe_id=obj.pk).exists()
        except Exception:
            return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'ingredients', 'name', 'image',
            'text', 'tags', 'cooking_time',
            'is_in_shopping_cart', 'is_favorite', 'author'
            )


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagRecipeSerializer(many=True, required=False)
    ingredients = IngredientRecipeSerializer(many=True)
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart'
    )
    is_favorite = serializers.SerializerMethodField('get_is_favorite')

    class Meta:
        fields = (
            'id', 'ingredients', 'name', 'image',
            'text', 'tags', 'cooking_time',
            'is_in_shopping_cart', 'is_favorite', 'author'
            )
        model = Recipe

    def to_internal_value(self, data):
        """Удаляем теги из даты, чтобы корректно серилиазовалось поле картинки, а затем добавляем теги обратно."""
        tags = data.pop('tags')
        internal_data = super().to_internal_value(data)
        internal_data['tags'] = tags
        return internal_data

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            tag_obj = get_object_or_404(Tag, id=tag)
            TagRecipe.objects.create(
                tag=tag_obj, recipe=recipe
            )
        for ingredient in ingredients:
            amount = ingredient['amount']
            current_ingredient = ingredient['id']
            ingr_obj = get_object_or_404(Ingredient, id=current_ingredient)
            IngredientRecipe.objects.create(
                ingredient=ingr_obj, recipe=recipe, amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        instance.amounts.all().delete()
        instance.tagrecipe_set.all().delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        Recipe.objects.filter(pk=instance.pk).update(**validated_data)
        for tag in tags:
            tag_obj = get_object_or_404(Tag, id=tag)
            TagRecipe.objects.create(tag=tag_obj, recipe=instance)
        for ingredient in ingredients:
            amount = ingredient['amount']
            current_ingredient = ingredient['id']
            ingr_obj = get_object_or_404(Ingredient, id=current_ingredient)
            IngredientRecipe.objects.create(
                ingredient=ingr_obj, recipe=instance, amount=amount
            )
        return get_object_or_404(Recipe, pk=instance.pk)

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(
            author=self.context['request'].user, recipe=obj
        ).exists()

    def get_is_favorite(self, obj):
        return FavoriteRecipes.objects.filter(
            author=self.context['request'].user, recipe=obj
        ).exists()


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'cooking_time', 'image')


class IsFavoriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True
    )
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.ImageField(source='recipe.image', read_only=True)

    class Meta:
        model = FavoriteRecipes
        fields = ('id', 'name', 'cooking_time', 'image')
