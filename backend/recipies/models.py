from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField('Название тега', max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True, default=None)
    hexcolor = models.CharField('Цвет', max_length=7, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента', max_length=100, blank=False, default=None
    )
    measurement_unit = models.CharField('Единицы измерения', max_length=50)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
        )
    name = models.CharField('Название рецепта', max_length=200)
    image = models.ImageField(
        'Изображение рецепта',
        upload_to='images',
        null=True,
        default=None
        )
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes'
    )
    cooking_time = models.IntegerField(verbose_name='Время приготовления')


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
        Ingredient, on_delete=models.CASCADE,
        related_name='amounts'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='amounts'
    )
    amount = models.PositiveSmallIntegerField('Количество', default=1)


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепты'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Владелец списка'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class FavoriteRecipes(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Списки избранных рецептов'


class Following(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_user_following"
            )
        ]

