from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import validate_year


class Category(models.Model):
    """Модель для категорий.
    Attributes:
        name: название категории.
        slug: уникальная строка категории.
    """
    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(
        'Слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Slug'
        verbose_name_plural = 'Slugs'

    def __str__(self):
        return f'{self.name} {self.name}'


class Genre(models.Model):
    """Модель для жанров.
    Attributes:
        name: название жанра.
        slug : уникальная строка жанра.
    """
    name = models.CharField(
        'Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        'Слаг жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    """Модель для произведений.
    Attributes:
        name: название произведения.
        year: год публикации.
        category: категория.
        description: описание.
        genre: жанр.
    """
    name = models.CharField(
        'Название произведения',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField(
        'Год',
        validators=(validate_year, )
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для отзывов.
    Attributes:
        title: привязанное к отзыву произведение.
        text: текст отзыва.
        author: автор.
        score: оценка.
        pub_date: дата публикации.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1, message="Оценка ниже 1, невозможна"),
            MaxValueValidator(10, message="Оценка больше 10, невозможна")
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для комментариев к отзывам.
    Attributes:
        review: привязанный к комментарию отзыв.
        text: текст комментария.
        author: автор.
        pub_date: дата публикации.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
