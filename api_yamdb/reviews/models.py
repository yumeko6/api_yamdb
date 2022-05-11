from django.core.validators import MinValueValidator
from django.db import models

from .validators import current_year_validator


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        'Наименование категории',
        max_length=256
    )
    slug = models.SlugField(
        'Адрес категории',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        'Наименование жанра',
        max_length=256
    )
    slug = models.SlugField(
        'Адрес жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='category',
        blank=True,
        null=False,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    name = models.CharField(
        'Название произведения',
        max_length=256,
        blank=False
    )
    year = models.PositiveIntegerField(
        'Год выпуска',
        db_index=True,
        validators=(
            MinValueValidator(862),
            current_year_validator
        ),
    )
    rating = models.IntegerField(
        'Рейтинг поста',
        null=True
    )
    description = models.TextField(
        'Описание произведения',
        blank=True
    )

    class Meta:
        ordering = ('year', )
        verbose_name = 'Произведения'

    def __str__(self):
        return f'Произведение {self.name}, рейтинг {self.rating}'


class GenreTitle(models.Model):
    """Связанная таблица жанров и произведений."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name='genre',
        blank=True,
        null=False,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('genre', )
        verbose_name = 'Жанры произведений'

    def __str__(self):
        return f'{self.genre} {self.title}'
