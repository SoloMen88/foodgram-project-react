from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator
    email = models.EmailField(
        'Почта', max_length=254, unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(
        'Имя', max_length=150,
    )
    last_name = models.CharField(
        'Фамилия', max_length=150,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    def __str__(self):
        return self.email
