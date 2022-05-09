from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Username',
        max_length=255,
        unique=True
    )
    email = models.EmailField(
        'Email Address',
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.TextField(
        'Роль',
        blank=True,
    )
