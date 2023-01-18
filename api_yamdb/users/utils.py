from django.core.mail import send_mail
from django.template.loader import get_template

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Получение JWT токенов."""
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_confirm_code(username, email, confirmation_code):
    """Отправление письма с кодом подтверждения."""
    current_context = {'username': username,
                       'confirmation_code': confirmation_code}
    send_mail(
        subject='Код для подтверждения учетной записи yambd',
        message=None,
        recipient_list=[email, ],
        from_email=None,
        fail_silently=False,
        html_message=get_template('conf_email.html').render(current_context)
    )
