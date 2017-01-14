from django.test import tag
from django.test import Client
from django.contrib.auth.models import User

from qua.api.tests.common import BaseQuaTestCase


@tag('auth', 'ready')
class AuthTest(BaseQuaTestCase):
    def test_auth_failed_when_no_credentials(self):
        resp = self.client.get('/api/categories')

        self.assertEquals(resp.status_code, 401)
        self.assertEquals(resp.data['error']['error_msg'],
            'Authentication credentials were not provided.')

    def test_auth_process(self):
        resp = self.auth()

        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', resp.data['response'])

    def test_auth_failed_when_password_wrong(self):
        resp = self.auth(password='wrong')

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data['error']['error_msg'],
            'Unable to login with provided credentials.')

    def test_disabled_user_auth_fail(self):
        user = User.objects.get(pk=2)
        auth = self.auth('test2', 'test2').json()
        token = auth['response']['token']

        user.is_active = False
        user.save()

        c = Client(HTTP_AUTHORIZATION='JWT ' + token)

        resp = c.get('/api/categories')

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.data['error']['error_msg'], 'User account is disabled.')
