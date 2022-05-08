from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(
        'Уникальный адрес адрес',
        max_length=30,
        unique=True
        )

    class Meta:
        verbose_name = 'Категория'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        'Название жанра',
        max_length=256)
    slug = models.SlugField(
        'Уникальный адрес жанра',
        max_length=30,
        unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Жанры'

    def __str__(self) -> str:
        return self.name


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
