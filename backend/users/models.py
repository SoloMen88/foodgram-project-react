from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Почта')
    username = models.CharField(max_length=150, unique=True,
                                validators=[username_validator],
                                verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
