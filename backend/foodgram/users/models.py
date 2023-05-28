"""Импорт и переопределение модели AbstractUser."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from users.validators import validate_email_address, validate_username


class User(AbstractUser):
    """
    Переопределенный класс пользователя.
    """

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Укажите адрес электронной почты',
        unique=True,
        null=False,
        max_length=254,
        validators=[
            validate_email_address
        ]
    )

    username = models.CharField(
        max_length=150,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
        null=False,
        validators=[
            validate_username
        ]
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Укажите Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Укажите Фамилию',
        blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'username', 'first_name', 'last_name']

    def __str__(self):
        """Возвращает никнейм пользователя."""
        return self.username

    class Meta:
        """Метакласс переопределнной модели User."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)


class Subscription(models.Model):
    """Модель подписки пользователя на автора."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        """Метакласс подписки на пользователя."""
        ordering = ['-id']
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
