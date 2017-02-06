from django.urls import reverse
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from qua import utils


class Command(BaseCommand):

    help = 'Reset password or create new user'

    def _generate_reset_link(self, user):

        user_id = user.id
        current_password = user.password

        token = utils.sign('{0}-{1}'.format(user_id, current_password))

        url = '{0}?token={1}'.format(
            reverse('password_reset', kwargs={'user_id': user_id}),
            token
        )

        return url

    def add_arguments(self, parser):

        parser.add_argument('-u', '--user',
            type=str, help='Username', required=True
        )
        parser.add_argument('-c', '--create',
            action='store_true', help='Create user'
        )

    def handle(self, *args, **options):

        username = options['user']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is None:
            if options['create']:
                user = User.objects.create_user(username)
            else:
                self.stdout.write(
                    self.style.ERROR(
                        'User `{0}` does not exists. Use ' \
                        '`-c` to create it'.format(username)
                    )
                )
                return None
        else:
            user.set_unusable_password()
            user.save()

        self.stdout.write(
            self.style.SUCCESS(
                'Reset link: {0}'.format(self._generate_reset_link(user))
            )
        )
