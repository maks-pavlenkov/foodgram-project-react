from rest_framework import serializers
from users.models import User
from recipies.models import (Ingredient, IngredientRecipe, Recipe, Tag,
                             TagRecipe, ShoppingCart, FavoriteRecipes, Following)


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
        representation['hexcolor'] = instance.hexcolor
        representation['slug'] = instance.slug

        return representation

# class TagRecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ('')

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagRecipeSerializer(many=True, required=False)
    ingredients = IngredientRecipeSerializer(many=True)
    is_in_shopping_cart = serializers.SerializerMethodField('get_is_in_shopping_cart')
    is_favorite = serializers.SerializerMethodField('get_is_favorite')

    class Meta:
        fields = (
            'id', 'ingredients', 'name', 'image', 
            'description', 'tags', 'time_to_cook', 
            'is_in_shopping_cart', 'is_favorite'
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
            # current_tag, status = Tag.objects.get_or_create(
            #     **tag)
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
    
    def get_is_in_shopping_cart(self, obj):
        print(self.context)
        return ShoppingCart.objects.filter(author=self.context['request'].user, recipe=obj).exists()
    
    def get_is_favorite(self, obj):
        return FavoriteRecipes.objects.filter(author=self.context['request'].user, recipe=obj).exists()


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
    time_to_cook = serializers.SlugRelatedField(source='recipe', read_only=True, slug_field='time_to_cook')
    name = serializers.SlugRelatedField(source='recipe', read_only=True, slug_field='name')

    class Meta:
        model = FavoriteRecipes
        fields = ('id', 'name', 'time_to_cook')

class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'image', 'cooking_time')
    
    # def validate_na(self, value):
    #     print(value, 'VALIDATE_NAME')
    #     return value

class SubscriptionsSerializer(serializers.ModelSerializer):
    # username = serializers.SlugRelatedField(source='user', slug_field='username', read_only=True)
    # first_name = serializers.SlugRelatedField(source='user', slug_field='first_name', read_only=True)
    # last_name = serializers.SlugRelatedField(source='user', slug_field='last_name', read_only=True)
    # email = serializers.SlugRelatedField(source='user', slug_field='email', read_only=True)
    # username = serializers.SlugRelatedField(source='user', slug_field='username', read_only=True)
    recipes = RecipeSubscriptionSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username',
                  'recipes')
    
    def validate_users(self, value):
        print(value, 'VALIDATE_USERS')
        return value
    
    def validate(self, data):
        print(data, 'VALIDATE_DATA')
        return data
    
    def to_internal_value(self, data):
        print(data, 'TO_INTERNAL_VALUE')
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        obj = super(SubscriptionsSerializer, self).to_representation(instance)
        print(obj, 'TO_REPRESENTATION')
        return obj


class SubscribeSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(source='user', slug_field='username', read_only=True)

    class Meta:
        model = Following
        fields = ('id', 'username')