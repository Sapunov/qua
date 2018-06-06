from datetime import timedelta
from smtplib import SMTPException
import binascii
import os

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.db.models.signals import post_save
from django.dispatch import receiver
import user_agents

from app import misc
from app.common import get_logger
from .authentication import retrieve_auth_token


log = get_logger(__name__)


class User(AbstractUser):

    _reset_password_token = models.CharField(max_length=64, unique=True, null=True, default=None)
    _reset_password_token_valid_until = models.DateTimeField(null=True, default=None)

    @classmethod
    def email_exists(cls, email):

        return cls.objects.filter(email=email).exists()

    @classmethod
    def username_exists(cls, username):

        return cls.objects.filter(username=username).exists()

    def _generate_reset_password_token(self):

        token = misc.get_random_string(64)

        # Для того чтобы токен был уникальным точно
        while User.objects.filter(_reset_password_token=token).exists():
            token = misc.get_random_string(64)

        self._reset_password_token = token
        self._reset_password_token_valid_until = timezone.now() + \
            timedelta(days=settings.RESET_PASSWORD_TOKEN_VALID_DAYS)

        self.save()

    def is_reset_password_token_expired(self):

        return self._reset_password_token_valid_until < timezone.now()

    def get_or_create_reset_password_token(self, dont_create=False):

        if (self._reset_password_token is None
                or self.is_reset_password_token_expired()) \
                and not dont_create:
            self._generate_reset_password_token()

        return self._reset_password_token

    def generate_reset_password_link(self, request):

        reset_password_url = request.build_absolute_uri(
            settings.RESET_PASSWORD_URL)

        return misc.add_param_to_url(
            reset_password_url,
            'token',
            self.get_or_create_reset_password_token())

    def send_reset_password_link(self, request, invite=False):

        reset_link = self.generate_reset_password_link(request)

        if invite:
            subject = 'Приглашение в QUA'
            template = get_template('emails/invite.html')
        else:
            subject = 'Сброс пароля в QUA'
            template = get_template('emails/reset_password.html')

        try:
            send_mail(
                subject,
                'Ссылка для сброса пароля в QUA: {0}'.format(reset_link),
                'robot@qua-engine.com',
                [self.email],
                fail_silently=False,
                html_message=template.render({'reset_password_link': reset_link})
            )
        except SMTPException as exc:
            log.exception(exc)

    def set_password(self, *args, **kwargs):

        super().set_password(*args, **kwargs)
        self._reset_password_token = None
        self._reset_password_token_valid_until = None

        self.save()

    def get_sessions(self, request):

        token = retrieve_auth_token(
            misc.get_header(request, 'HTTP_AUTHORIZATION'))

        assert token is not None, 'Token can not be None'

        sessions = self.sessions.all()
        for session in sessions:
            session.current = session.access_token == token

        return sessions


class UserSession(models.Model):

    access_token = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    created = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=500, null=True)
    ip_address = models.CharField(max_length=20, null=True)
    last_use = models.DateTimeField(auto_now_add=True)
    browser = models.CharField(max_length=50, null=True)
    browser_version = models.CharField(max_length=10,  null=True)
    os = models.CharField(max_length=50, null=True)
    os_version = models.CharField(max_length=10, null=True)

    @property
    def browser_full(self):

        return '{0} ({1})'.format(self.browser, self.browser_version)

    @property
    def os_full(self):

        return '{0} ({1})'.format(self.os, self.os_version)

    def save(self, *args, **kwargs):

        if not self.pk:
            self.access_token = self.generate_key()

        ua = user_agents.parse(self.user_agent)

        self.browser = ua.browser.family
        self.browser_version = ua.browser.version_string
        self.os = ua.os.family
        self.os_version = ua.os.version_string

        return super(UserSession, self).save(*args, **kwargs)

    def generate_key(self):

        return binascii.hexlify(os.urandom(20)).decode()

    def mark_last_use(self):

        self.last_use = timezone.now()
        self.save()

    def __str__(self):

        return self.access_token
