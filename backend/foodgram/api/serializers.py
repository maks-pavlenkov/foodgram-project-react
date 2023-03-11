from rest_framework import serializers
from recipies.models import (Ingredient, IngredientRecipe, Recipe, Tag,
                             TagRecipe)


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

    class Meta:
        fields = ('id', 'ingredients', 'name', 'image', 'description', 'tags', 'time_to_cook')
        model = Recipe

    # def get_tags(self, obj):
    #     return TagSerializer(obj.tags).data

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
