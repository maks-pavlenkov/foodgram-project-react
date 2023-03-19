import base64
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from users.models import User
from .fields import Base64ImageField
from django.core.files.base import ContentFile
from recipies.models import (Ingredient, IngredientRecipe, Recipe, Tag,
                             TagRecipe, ShoppingCart, FavoriteRecipes, Following)
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            forma, imgstr = data.split(';base64,')
            ext = forma.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'units')
        model = Ingredient


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())

    class Meta:
        fields = ('id', 'amount')
        model = IngredientRecipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tag

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.name
        representation['hexcolor'] = instance.hexcolor
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
        representation['hexcolor'] = instance.hexcolor
        representation['slug'] = instance.slug

        return representation

# class TagRecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ('')

class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagRecipeSerializer(many=True, required=False)
    ingredients = IngredientRecipeSerializer(many=True)
    is_in_shopping_cart = serializers.SerializerMethodField('get_is_in_shopping_cart')
    is_favorite = serializers.SerializerMethodField('get_is_favorite')

    class Meta:
        fields = (
            'id', 'ingredients', 'name', 'image', 
            'description', 'tags', 'time_to_cook', 
            'is_in_shopping_cart', 'is_favorite', 'author'
            )
        model = Recipe

    def create(self, validated_data): 
        if 'tags' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            TagRecipe.objects.create(
                tag=tag['id'], recipe=recipe
            )
        for ingredient in ingredients:
            amount = ingredient['amount']
            current_ingredient = ingredient['id']
            IngredientRecipe.objects.create(
                ingredient=current_ingredient, recipe=recipe, amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        instance.ingredientrecipe_set.all().delete()
        instance.tagrecipe_set.all().delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        Recipe.objects.filter(pk=instance.pk).update(**validated_data)
        for tag in tags:
            TagRecipe.objects.create(tag=tag['id'], recipe=instance)
        for ingredient in ingredients:
            amount = ingredient['amount']
            current_ingredient = ingredient['id']
            IngredientRecipe.objects.create(
                ingredient=current_ingredient, recipe=instance, amount=amount
            )
        return get_object_or_404(Recipe, pk=instance.pk)

    def get_is_in_shopping_cart(self, obj):
        print(self.context)
        return ShoppingCart.objects.filter(
            author=self.context['request'].user, recipe=obj
        ).exists()

    def get_is_favorite(self, obj):
        return FavoriteRecipes.objects.filter(
            author=self.context['request'].user, recipe=obj
        ).exists()


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.SlugRelatedField(source='recipe', read_only=True, slug_field='name')
    # image = serializers.SlugRelatedField(source='recipe', read_only=True, slug_field='image')
    time_to_cook = serializers.SlugRelatedField(source='recipe', read_only=True, slug_field='time_to_cook')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'time_to_cook')

class IsFavoriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    time_to_cook = serializers.IntegerField(source='recipe.time_to_cook', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.ImageField(source='recipe.image', read_only=True)

    class Meta:
        model = FavoriteRecipes
        fields = ('id', 'name', 'time_to_cook', 'image')

class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'time_to_cook')
    
    # def validate_users(self, value):
    #     print(value, 'VALIDATE_USERS')
    #     return value
    
    # def validate(self, data):
    #     print(data, 'VALIDATE_DATA')
    #     return data
    
    # def to_internal_value(self, data):
    #     print(data, 'TO_INTERNAL_VALUE')
    #     return super().to_internal_value(data)
    
    # def validate_na(self, value):
    #     print(value, 'VALIDATE_NAME')
    #     return value

class SubscriptionsSerializer(serializers.ModelSerializer):
    recipes = RecipeSubscriptionSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')


    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'is_subscribed',
                  'recipes')

    def get_is_subscribed(self, obj):
        print(obj, 'OBJ')
        print(self.context['request'].user, 'USER')
        return Following.objects.filter(
            user=self.context['request'].user, 
            following=obj
        ).exists()



        # def get_is_in_shopping_cart(self, obj):
        # print(self.context)
        # return ShoppingCart.objects.filter(
        #     author=self.context['request'].user, recipe=obj
        # ).exists()
    
    # def validate_users(self, value):
    #     print(value, 'VALIDATE_USERS')
    #     return value
    
    # def validate(self, data):
    #     print(data, 'VALIDATE_DATA')
    #     return data
    
    # def to_internal_value(self, data):
    #     print(data, 'TO_INTERNAL_VALUE')
    #     return super().to_internal_value(data)
    
    # def to_representation(self, instance):
    #     obj = super(SubscriptionsSerializer, self).to_representation(instance)
    #     print(obj, 'TO_REPRESENTATION')
    #     return obj


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = RecipeSubscriptionSerializer(many=True, required=False)

    username = serializers.SerializerMethodField('get_username')
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')
    email = serializers.SerializerMethodField('get_email')
    recipes = RecipeSubscriptionSerializer(many=True, required=False, read_only=True)


    class Meta:
        model = Following
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'recipes')
    
    def create(self, validated_data):
        user = validated_data.get('user', False)
        following = validated_data.get('following', False)
        if not following:
            raise serializers.ValidationError('Failed: No such user')
        if user == following:
            raise serializers.ValidationError(
                'Failed: You cant follow yourself!'
            )
        if Following.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                f'Failed: You already follow {following.username}'
            )
        return Following.objects.create(**validated_data)

    def get_username(self, obj):
        return obj.following.username

    def get_first_name(self, obj):
        return obj.following.first_name

    def get_last_name(self, obj):
        return obj.following.last_name

    def get_email(self, obj):
        return obj.following.email
