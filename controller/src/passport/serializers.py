from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import (ValidationError, PermissionDenied,
    AuthenticationFailed, NotFound)
from rest_framework.compat import authenticate

from app import misc

from .models import User, UserSession
from .authentication import retrieve_auth_token
from passport import exceptions


class UsernameExistsSerializer(serializers.Serializer):

    username = serializers.CharField()


class EmailExistsSerializer(serializers.Serializer):

    email = serializers.EmailField()


class UserSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    send_invite = serializers.BooleanField(default=False)

    def validate(self, attrs):

        username = attrs.get('username')
        email = attrs.get('email')

        if User.username_exists(username):
            raise ValidationError({
                'username': 'Username `%s` already exists' % username},
                'username_exists')

        if User.email_exists(email):
            raise ValidationError({
                'email': 'Email `%s` already exists' % email},
                'email_exists')

        # TODO: Проверка прав текущего пользователя
        # на создание новых пользователей

        return attrs

    def create(self, validated_data):

        user = User.objects.create_user(
            validated_data['username'],
            email=validated_data['email'])

        return user


class SetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(style={'input_type': 'password'})
    ensure_password = serializers.CharField(style={'input_type': 'password'})
    token = serializers.CharField()

    def validate(self, attrs):

        password = attrs.get('password')
        ensure_password = attrs.get('ensure_password')
        token = attrs.get('token')

        if password != ensure_password:
            raise ValidationError({
                'ensure_password': 'Passwords do not match'},
                'password_dont_match')

        invalid_token_msg =  {'token': 'Invalid token'}

        try:
            user = User.objects.get(_reset_password_token=token)
        except User.DoesNotExist:
            raise ValidationError(invalid_token_msg, 'token_invalid')

        if user.is_reset_password_token_expired():
            raise ValidationError(invalid_token_msg, 'token_invalid')

        attrs['user'] = user

        return attrs


class ObtainResetTokenSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate(self, attrs):

        email = attrs.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({
                'email': 'User with the specified email does not exist'},
                'user_does_not_exist')

        attrs['user'] = user

        return attrs


class ObtainResetTokenAuthorizedSerializer(serializers.Serializer):

    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):

        password = attrs.get('password')
        user = self.context['request'].user

        if not user.check_password(password):
            raise PermissionDenied({'password': ['Wrong password']})

        attrs['token'] = user.get_or_create_reset_password_token()

        return attrs


class ObtainAccessTokenSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False)

    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password)

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            msg = 'Unable to log in with provided credentials'
            raise AuthenticationFailed(msg, code='authorization')

        attrs['user'] = user

        return attrs


class UserSessionsSerializer(serializers.ModelSerializer):

    current = serializers.BooleanField()

    class Meta:

        model = UserSession
        fields = (
            'id', 'created', 'user_agent', 'ip_address',
            'current', 'last_use', 'browser',
            'browser_version', 'os', 'os_version')


class IndividualUserSessionSerializer(serializers.Serializer):

    session_id = serializers.CharField()

    def validate(self, attrs):

        session_id = attrs.get('session_id')
        request = self.context.get('request')
        user = request.user

        session_id = session_id.lower()

        if session_id == 'current':
            session = [sess for sess in user.get_sessions(request) \
                if sess.current][0]
        elif not session_id.isdigit():
            raise ValidationError({'session_id': 'Not a number'}, 'not_number')
        else:
            session_id = int(session_id)
            try:
                session = UserSession.objects.get(pk=session_id)
            except UserSession.DoesNotExist:
                raise NotFound(
                    'Session with session_id %s not found' % session_id)

        attrs['session'] = session

        return attrs
