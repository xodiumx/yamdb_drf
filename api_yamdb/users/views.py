from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from .models import User
from .permissions import SuperUserOrAdmin, UserIsAuthenticated
from .serializers import (
    UserSerializer,
    UserIsNotAdminSerializer,
    SignUpSerializer,
    ReceiveJWTSerializer,
)


class BaseUserViewSet(CreateModelMixin,
                      ListModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet,):
    """Базовый ViewSet-для реализации CRUD."""
    ...


class UserViewSet(BaseUserViewSet):
    """
    /users/

    GET - Получить список всех пользователей. Права доступа: Администратор.
    POST - Добавить нового пользователя.
           Права доступа: Администратор
           Поля email и username должны быть уникальными.

    /users/{username}/

    GET - Получить пользователя по username. Права доступа: Администратор
    PATCH - Изменить данные пользователя по username.
            Права доступа: Администратор.
            Поля email и username должны быть уникальными.
    DELETE - Удалить пользователя по username. Права доступа: Администратор.

    /users/me/

    GET - Получить данные своей учетной записи Права доступа:
          Любой авторизованный пользователь
    PATCH - Изменить данные своей учетной записи
            Права доступа: Любой авторизованный пользователь
            Поля email и username должны быть уникальными.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete',)
    permission_classes = (SuperUserOrAdmin,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=('GET', 'PATCH'),
        detail=False,
        permission_classes=(UserIsAuthenticated,),
        url_path='me')
    def me(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True)
        if request.method == 'PATCH':
            if not request.user.is_admin and not request.user.is_superuser:
                serializer = UserIsNotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class SignUpViewSet(BaseUserViewSet):
    """
    POST - Получить код подтверждения на переданный email.
           Права доступа: Доступно без токена.
           Использовать имя 'me' в качестве username запрещено.
           Поля email и username должны быть уникальными.
    """
    serializer_class = SignUpSerializer
    http_method_names = ('post',)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(request.data, HTTP_200_OK)


class ReceiveJWTViewSet(TokenObtainPairView):
    """
    POST - Получение JWT-токена в обмен на username и confirmation code.
           Права доступа: Доступно без токена.
    """
    serializer_class = ReceiveJWTSerializer
    http_method_names = ('post',)
