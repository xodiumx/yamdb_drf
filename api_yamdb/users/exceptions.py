from rest_framework.exceptions import ValidationError


class UserFound(ValidationError):
    ...


class WrongData(ValidationError):
    ...


class NotValidUserName(ValidationError):
    ...
