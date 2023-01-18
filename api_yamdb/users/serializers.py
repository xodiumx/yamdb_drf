from re import match

from django.contrib.auth.tokens import default_token_generator
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField
)

from .exceptions import (
    UserFound,
    WrongData,
    NotValidUserName,
)
from .models import User
from .utils import get_tokens_for_user, send_confirm_code


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')


class UserIsNotAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        read_only_fields = ('role',)


class SignUpSerializer(Serializer):

    username = CharField(max_length=150)
    email = EmailField(max_length=254)

    def validate(self, data):
        """Валидируем username."""
        username = data['username']
        if username.lower() == 'me':
            raise NotValidUserName('Username "me" запрещен')
        if match(r'^[\w.@+-]+', data['username']) is None:
            raise NotValidUserName('Не корректный username')
        return data

    def create(self, validated_data):
        """
        - Если пользователя зарегестрировал admin
          генерируем токен, отправляем письмо на почту
          и получаем данные из запроса
        - Если пользователь регистрируется самостоятельно
          создаем пользователя в бд, генерируем токен, отправляем письмо
          и получаем данные из запроса
        """
        email = validated_data['email']
        username = validated_data['username']

        try:
            user, _ = User.objects.get_or_create(**validated_data)
            confirmation_code = default_token_generator.make_token(user)
            send_confirm_code(username, email, confirmation_code)
            return validated_data

        except IntegrityError:
            raise UserFound(
                'Пользователь с таким username или email существует')


class ReceiveJWTSerializer(Serializer):

    username = CharField(max_length=150)
    confirmation_code = CharField(max_length=50)

    def validate(self, data):
        """
        - Если пользователь есть в бд, выдаем токены, иначе 404 ошибка.
        - Если введен не правильный(истекший токен) - 400 ошибка.
        """
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            tokens = get_tokens_for_user(user)
            return {'tokens': tokens}
        else:
            raise WrongData('Введены не правильные данные или токен истек')
