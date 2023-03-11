from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, default=None)
    hexcolor = models.CharField(max_length=7)

class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=False, default=None)
    units = models.CharField(max_length=50)

class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='recipies/images',
        null=True,
        default=None
    )
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe')
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    time_to_cook = models.IntegerField()

class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )
    amount = models.IntegerField(null=True, blank=True)