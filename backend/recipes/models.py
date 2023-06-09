from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from foodgram.settings import MAX_LENGTH_TEXT, MAX_LENGTH_HEX

User = get_user_model()


class Ingredient(models.Model):
    """Модель Ингридента."""
    name = models.CharField(
        max_length=MAX_LENGTH_TEXT,
        verbose_name='Ингридиент'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_TEXT,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        """Возвращает название Ингридента"""
        return self.name


class Tag(models.Model):
    """Модель Тэга."""
    name = models.CharField(
        max_length=MAX_LENGTH_TEXT,
        unique=True,
        verbose_name='Название тэга'
    )
    color = ColorField(
        verbose_name='Цвет',
        format='hex',
        max_length=MAX_LENGTH_HEX
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_TEXT,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        """Возвращает имя Тега."""
        return self.name


class Recipe(models.Model):
    """Модель Рецепта."""
    name = models.CharField(
        max_length=MAX_LENGTH_TEXT,
        verbose_name='Название',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги рецепта')
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientAmount',
        verbose_name='Ингридиенты в рецепте',
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата'
    )
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=True,
        verbose_name='Картинка рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                1,
                message='Минимальное время 1 минута!'
            ),
        ],
        verbose_name='Время приготовления (в минутах)',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """Возвращает название Рецепта."""
        return self.name


class IngredientAmount(models.Model):
    """Модель количества ингридиентов в рецепте."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное количество ингридиентов 1'
            ),
        ),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ['amount']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredients_recipe')
        ]

    def __str__(self):
        """Возвращает строку Рецепт - Ингридиент в нём."""
        return f'{self.recipe} - {self.ingredient}'


class Favorite(models.Model):
    """Модель для избранного рецепта."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт автора',
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_name_favorite'
            )
        ]

    def __str__(self):
        """Возвращает связь Автор - Рецепт."""
        return f'{self.user} - {self.recipe}'


class ShoppingСart(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь сайта',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт в корзине пользователя',
    )

    class Meta:
        verbose_name = 'Cписок покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique cart user'
            )
        ]

    def __str__(self):
        """Возвращает список покупок пользователя."""
        return f'{self.user} - {self.recipe}'
