from django.contrib.auth.models import User
from django.test import tag
from rest_framework.test import APIClient

from api.tests.common import BaseQuaTestCase


@tag('auth')
class AuthTest(BaseQuaTestCase):

    def test_auth_failed_when_no_credentials(self):

        resp = self.client.get('/questions')

        self.assertEquals(resp.status_code, 401)
        self.assertEquals(
            resp.data['error']['error_msg'],
            'Authentication credentials were not provided.')

    def test_auth_process(self):

        resp = self.auth()

        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', resp.data['response'])

    def test_auth_failed_when_password_wrong(self):

        resp = self.auth(password='wrong')

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.data['error']['error_msg'],
            'Unable to log in with provided credentials.')

    def test_disabled_user_auth_fail(self):

        user = User.objects.get(username='test2')
        auth = self.auth('test2', 'test2').json()
        token = auth['response']['token']

        user.is_active = False
        user.save()

        c = APIClient(HTTP_AUTHORIZATION='JWT ' + token)

        resp = c.get('/questions')

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(
            resp.data['error']['error_msg'], 'User account is disabled.')

    def test_token_verification_works(self):

        resp = self.auth()
        token = resp.data['response']['token']

        client = APIClient()

        verify_resp = client.post('/token-verify', {'token': token})

        self.assertEqual(verify_resp.status_code, 200)

        verify_response = verify_resp.data['response']

        self.assertEqual(verify_response['token'], token)

    def test_token_verification_fail(self):

        resp = self.auth()
        token = resp.data['response']['token']

        client = APIClient()

        verify_resp = client.post('/token-verify', {'token': token + '#'})

        self.assertEqual(verify_resp.status_code, 400)

        verify_error_msg = verify_resp.data['error']['error_msg']

        self.assertEqual(verify_error_msg, 'Error decoding signature.')
