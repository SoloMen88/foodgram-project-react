from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Описание'
    )

    color = ColorField(
        unique=True, verbose_name='Цвет'
    )

    slug = models.SlugField(
        unique=True, max_length=254, verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(
        max_length=200, verbose_name='Название ингредиента'
    )

    measurement_unit = models.CharField(
        max_length=20, verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Описание'
    )

    image = models.ImageField(
        upload_to='foodgram/media/',
        verbose_name='Изображение'
    )

    text = models.TextField(verbose_name='Описание')

    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты'
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )

    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Количество не может быть меньше 1')],
        default=1,
        verbose_name='Время приготовления'
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_followings'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент в рецепте'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.SmallIntegerField(
        default=1,
        verbose_name='Количество ингредиента'
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredients'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipe_subscriber'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Рецепт {self.recipe} находится в  избранном у {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, related_name='customer',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, related_name='cart',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='recipe_unique'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Рецепт {self.recipe} в корзине у пользователя {self.user}'
