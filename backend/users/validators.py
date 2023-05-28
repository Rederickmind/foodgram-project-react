"""Валидаторы для данных пользователя."""
import re

from django.core.exceptions import ValidationError


def validate_username(username):
    """
    Валидация имени пользователя.

    Запрет на использования me в качетсве имени пользователя.
    Ограничение разрешенных символов в username.
    """
    if username.lower() == 'me':
        raise ValidationError(
            'Нельзя использовать "me" в качестве username!'
        )
    if not bool(
        re.fullmatch(
            r'^[\w.@+-]+$',
            username
        )
    ):
        raise ValidationError(
            'Некорректные символы в username'
        )
    return username


def validate_email_address(email_address):
    """
    Валидация электронной почты пользователя.

    Проверка на соответствие шаблону example@domen.region
    """
    if not bool(
        re.fullmatch(
            r'^[\w.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            email_address
        )
    ):
        raise ValidationError(
            'Некорректные символы в email'
        )
    return email_address
