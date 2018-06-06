from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from app import misc


HEADER_TOKEN_KEYWORD = 'Token'


def retrieve_auth_token(header_string):
    '''Возвращает None если строка пустая или
    первое слово строки не HEADER_TOKEN_KEYWORD.
    Поднимает ValueError, если строка токена имеет неверный формат
    '''

    if not header_string:
        return None

    parts = header_string.split()

    if not parts or parts[0].lower() != HEADER_TOKEN_KEYWORD.lower():
        return None

    if len(parts) == 1:
        msg = 'Invalid token header. No credentials provided'
        raise ValueError(msg)
    elif len(parts) > 2:
        msg = 'Invalid token header. Token string should not contain spaces'
        raise ValueError(msg)

    return parts[1]


class TokensAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_string = misc.get_header(request, 'HTTP_AUTHORIZATION')

        try:
            token = retrieve_auth_token(auth_string)
        except ValueError as exc:
            raise AuthenticationFailed(str(exc))

        if token is None:
            return None

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):

        from .models import UserSession

        try:
            session =  UserSession.objects.get(access_token=key)
        except UserSession.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        session.mark_last_use()

        if not session.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        return (session.user, None)

    def authenticate_header(self, request):

        return HEADER_TOKEN_KEYWORD
