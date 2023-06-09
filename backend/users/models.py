"""Импорт и переопределение модели AbstractUser."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from users.validators import validate_email_address, validate_username
from foodgram.settings import MAX_LENGTH_EMAIL, MAX_LENGTH_USER_NAMES_INFO


class User(AbstractUser):
    """
    Переопределенный класс пользователя.
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Укажите адрес электронной почты',
        unique=True,
        null=False,
        max_length=MAX_LENGTH_EMAIL,
        validators=[
            validate_email_address
        ]
    )

    username = models.CharField(
        max_length=MAX_LENGTH_USER_NAMES_INFO,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
        null=False,
        validators=[
            validate_username
        ]
    )

    first_name = models.CharField(
        max_length=MAX_LENGTH_USER_NAMES_INFO,
        verbose_name='Имя',
        help_text='Укажите Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_USER_NAMES_INFO,
        verbose_name='Фамилия',
        help_text='Укажите Фамилию',
        blank=True)

    def __str__(self):
        """Возвращает никнейм пользователя."""
        return self.username

    class Meta:
        """Метакласс переопределнной модели User."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', 'first_name', 'last_name')
        constraints = [
            UniqueConstraint(
                fields=['email', 'username'],
                name='unique_user',
            )
        ]


class Subscription(models.Model):
    """Модель подписки пользователя на автора."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    def __str__(self):
        """Возвращает сообщение о подписке пользователя на автора."""
        return f'Пользователь {self.user} подписался на {self.author}'

    class Meta:
        """Метакласс подписки на пользователя."""
        ordering = ['-id']
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe',
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
