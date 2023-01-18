from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField, EmailField

from .validators import validate_username

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_PERMISSION = [
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор')
]


class User(AbstractUser):
    """Модель для пользователей.

    Attributes:
        username: отображаемое имя пользователя.
        email: почта пользователя.
        first_name: имя.
        last_name: фамилия.
        bio: биография.
        role: роль(права доступа).
    """

    username = CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=(validate_username,),
    )
    email = EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = TextField(
        'Биография',
        blank=True,
    )
    role = CharField(
        'Роль',
        max_length=20,
        choices=ROLE_PERMISSION,
        default=USER,
        blank=True,
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = ('User')
        verbose_name_plural = ('Users')

    def __str__(self):
        return self.username
