from django.contrib import admin

from .models import Title, Category, Genre, Comment, Review


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Конфигурация отображения данных.

    Attributes:
        list_display: отображаемые поля.
        search_fields: интерфейс для поиска по названию.
        list_filter: возможность фильтрации по названию.
    """

    list_display = (
        'name',
        'year',
        'category',
        'description',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Конфигурация отображения данных.

    Attributes:
        list_display: отображаемые поля.
        search_fields: интерфейс для поиска по названию.
        list_filter: возможность фильтрации по названию.
    """

    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Конфигурация отображения данных.

    Attributes:
        list_display: отображаемые поля.
        search_fields: интерфейс для поиска по названию.
        list_filter: возможность фильтрации по названию.
    """

    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Конфигурация отображения данных.

    Attributes:
        list_display: отображаемые поля.
        search_fields: интерфейс для поиска по дате.
        list_filter: возможность фильтрации по дате.
    """

    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Конфигурация отображения данных.

    Attributes:
        list_display: отображаемые поля.
        search_fields: интерфейс для поиска по отзыву.
        list_filter: возможность фильтрации по отзыву.
    """

    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'
