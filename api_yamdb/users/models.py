from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'Email Address',
        max_length=254,
        unique=True
    )
    confirmation_code = models.TextField(
        blank=True,
        verbose_name='Код подтверждения'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.TextField(
        'Роль',
        blank=True,
        default='user'
    )
