import csv
import os

import django.db.utils
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from reviews.models import Title, Category, Genre, Review, Comment
from users.models import User

DATA_TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


def read_csv(name_file):
    """
    Считывание данных из csv и возвращение списока строк таблицы.
    """

    path = os.path.join('static/data', name_file)
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        return list(reader)


def get_list_fields_model(model):
    """
    Принимает объект модели, и возвращает словарь с полями в виде:
    {<поле модели>: <поле в таблице>}.
    """

    fields_obj_list = model._meta.fields
    fields = {
        field.name: field.attname for field in fields_obj_list
    }
    return fields


def changes_fields(fields_model, table):
    """
    Изменение названий полей таблицы
    для корректной записи в БД.
    """

    for row in table:
        for name_field in list(row):
            if (
                name_field in fields_model
                and name_field
                != fields_model[name_field.replace("_id", "")]
            ):
                row[fields_model[name_field]] = row.pop(name_field)


def load_data(model, name_file):
    """Загрузка данных по модели."""

    table = read_csv(name_file)
    changes_fields(get_list_fields_model(model), table)
    model.objects.bulk_create(model(**row) for row in table)


def load_genre_title():
    """
    Загрузка данных во вспомогательную таблицу
    со связью многие ко многим.
    """

    data_list = read_csv('genre_title.csv')
    [Title.objects.get(id=row['title_id']).genre.add(
        row['genre_id']) for row in data_list]


def del_data():
    """Удаление всех таблиц из базы данных."""

    for model in DATA_TABLES:
        model.objects.all().delete()


class Command(BaseCommand):
    help = 'Импорт данных из csv в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--load',
            action='store_true',
            help='Импорт всех таблиц из csv в базу данных'
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Удаление всех данных из базы данных'
        )

    def handle(self, *args, **options):
        try:
            if options['load']:
                for model, name_file in DATA_TABLES.items():
                    load_data(model, name_file)
                    print(f'Загрузка "{name_file}" выполнена')

                try:
                    load_genre_title()
                except Exception as error:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Ошибка при загрузке genre_title.csv: {error}'
                        )
                    )
                else:
                    print('Загрузка "genre_title.csv" выполнена')

                self.stdout.write(
                    self.style.SUCCESS('Данные загружены в базу данных.')
                )

            elif options['delete']:
                del_data()
                self.stdout.write(
                    self.style.SUCCESS('База данных удалена.')
                )
            else:
                self.stdout.write(
                    self.style.SQL_KEYWORD(
                        'Команда используется с ключом, '
                        'все ключи: python manage.py import_data --help'
                    )
                )

        except django.db.utils.IntegrityError as error:
            self.stdout.write(
                self.style.ERROR(
                    f'База данных не пуста. '
                    f'Совпадение уникальных полей. {error}'
                )
            )
        except ObjectDoesNotExist:
            self.stdout.write(
                self.style.NOTICE('Нет данных из связанных таблиц')
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(f'Ошибка загрузки данных: {error}')
            )
