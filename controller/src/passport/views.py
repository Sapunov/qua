from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from app.common import get_logger
from app.rest import QuaAPIResponse
from app import misc
from .serializers import (
    UsernameExistsSerializer, EmailExistsSerializer, UserSerializer,
    SetPasswordSerializer, ObtainResetTokenSerializer,
    ObtainResetTokenAuthorizedSerializer, ObtainAccessTokenSerializer,
    UserSessionsSerializer, IndividualUserSessionSerializer)
from .models import (User, UserSession)


log = get_logger(__file__)


class UsernameExistsView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UsernameExistsSerializer

    def get(self, request):

        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']

        return QuaAPIResponse(
            {
                'username': username,
                'username_exists': User.username_exists(username)
            },
            status=status.HTTP_200_OK
        )


class EmailExistsView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = EmailExistsSerializer

    def get(self, request):

        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        return QuaAPIResponse(
            {
                'email': email,
                'email_exists': User.email_exists(email)
            },
            status=status.HTTP_200_OK
        )


class UserView(GenericAPIView):

    serializer_class = UserSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        serializer.instance.send_reset_password_link(request, invite=True)

        return QuaAPIResponse({}, status=status.HTTP_200_OK)


class SetPasswordView(GenericAPIView):
    '''Установка нового пароля
    '''

    serializer_class = SetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['password'])

        return QuaAPIResponse({}, status=status.HTTP_200_OK)


class ObtainResetTokenView(GenericAPIView):
    '''Пользовательский запрос на получение токена для
       сброса пароля
    '''

    permission_classes = (AllowAny,)
    serializer_class = None

    def post(self, request):

        if request.user.is_anonymous:
            self.serializer_class = ObtainResetTokenSerializer
        else:
            self.serializer_class = ObtainResetTokenAuthorizedSerializer

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_anonymous:
            serializer.validated_data['user'].send_reset_password_link(request)
            return QuaAPIResponse(
                {'email_sent': True}, status=status.HTTP_200_OK)
        else:
            token = serializer.validated_data['token']
            return QuaAPIResponse(
                {'reset_password_token': token},
                status=status.HTTP_200_OK)


class ObtainAccessTokenView(GenericAPIView):
    '''Получение токена для доступа к защищаемым ресурсам
    '''

    permission_classes = (AllowAny,)
    serializer_class = ObtainAccessTokenSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        session = UserSession.objects.create(
            user=user,
            user_agent=misc.get_header(request, 'HTTP_USER_AGENT'),
            ip_address=misc.get_header(request, 'REMOTE_ADDR'))

        return QuaAPIResponse(
            {'access_token': session.access_token},
            status=status.HTTP_200_OK)


class UserSessionsView(GenericAPIView):

    serializer_class = UserSessionsSerializer

    def get(self, request):

        serializer = self.get_serializer(
            request.user.get_sessions(request), many=True)

        return QuaAPIResponse(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):

        for session in [sess for sess in request.user.get_sessions(request) \
                if not sess.current]:
            session.delete()

        return QuaAPIResponse({}, status=status.HTTP_200_OK)


class IndividualUserSessionView(GenericAPIView):

    serializer_class = IndividualUserSessionSerializer

    def delete(self, request, session_id):

        serializer = self.get_serializer(data={'session_id': session_id})
        serializer.is_valid(raise_exception=True)

        session = serializer.validated_data['session']
        session.delete()

        return QuaAPIResponse({}, status=status.HTTP_200_OK)
