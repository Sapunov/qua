from datetime import timedelta
import re

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core import mail
from django.conf import settings
from django.test import tag

from .models import User, UserSession


def extract_token(text):

    pattern = r'\?token=(.+)'
    result = re.search(pattern, text)

    return result.group(1) if result else None


def extract_dict_keys(input_dict):

    return sorted(list(input_dict.keys()))


class UsernameExistsTestCase(APITestCase):

    url = reverse('username_exists')

    def test_unique_username(self):

        user_data = {
            'username': 'user'
        }

        response = self.client.get(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response']['username_exists'], False)

        User.objects.create_user('user')

        response = self.client.get(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response']['username_exists'], True)

    def test_output_format(self):

        user_data = {
            'username': 'user'
        }

        response = self.client.get(self.url, user_data)

        expected_output = {
            'ok': 1,
            'response': {
                'username': 'user',
                'username_exists': False
            }
        }

        self.assertEqual(response.data, expected_output)

    def test_blank_username(self):

        user_data = {
            'username': ''
        }

        response = self.client.get(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmailExistsTestCase(APITestCase):

    url = reverse('email_exists')

    def test_unique_email(self):

        user_data = {
            'email': 'empty@gmail.com'
        }

        response = self.client.get(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response']['email_exists'], False)

        User.objects.create_user('user', email='empty@gmail.com')

        response = self.client.get(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response']['email_exists'], True)

    def test_blank_email(self):

        user_data = {
            'email': ''
        }

        response = self.client.get(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_email(self):

        user_data = {
            'email': 'empty@gmail'
        }

        response = self.client.get(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_output_format(self):

        user_data = {
            'email': 'empty@gmail.com'
        }

        response = self.client.get(self.url, user_data)

        expected_output = {
            'ok': 1,
            'response': {
                'email': 'empty@gmail.com',
                'email_exists': False
            }
        }

        self.assertEqual(response.data, expected_output)


class UserCreationTestCase(APITestCase):

    url = reverse('users')

    def setUp(self):

        self.username = 'qua_user'
        self.email = 'qua_user@gmail.com'
        self.password = 'qua_password'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = UserSession.objects.create(
            user=self.user,
            user_agent='',
            ip_address='').access_token

        self.api_authentication()

    def api_authentication(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_absent_arguments(self):

        user_data = {}
        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_username(self):

        user_data = {
            'username': '',
            'email': 'qua_user_2@gmail.com'
        }
        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_email(self):

        user_data = {
            'username': 'qua_user_2',
            'email': ''
        }
        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_token(self):

        username = 'qua_user_2'

        user_data = {
            'username': username,
            'email': 'qua_user_2@gmail.com'
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(
            User.objects.get(username=username)._reset_password_token)

    def test_email_send(self):

        user_data = {
            'username': 'qua_user_2',
            'email': 'qua_user_2@gmail.com'
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

        invite_mail = mail.outbox[0]
        token = extract_token(invite_mail.body)

        self.assertEqual(invite_mail.subject, 'Приглашение в QUA')
        self.assertIsNotNone(token)

    def test_success_output_format(self):

        user_data = {
            'username': 'qua_user_2',
            'email': 'qua_user_2@gmail.com'
        }

        expected_output = {
            'ok': 1,
            'response': {}
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_output, response.data)


    def test_method_auth(self):

        self.client.credentials() # Сброс токена
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SetPasswordTestCase(APITestCase):

    url = reverse('password_set')

    def setUp(self):

        self.username = 'qua_user'
        self.email = 'qua_user@gmail.com'
        self.password = 'qua_password'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = UserSession.objects.create(
            user=self.user,
            user_agent='',
            ip_address='').access_token

    def api_authentication(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_absent_arguments_anonymous(self):

        response = self.client.post(self.url, {})

        expected_output = {
            'ok': 0,
            'error': {
                'error_code': 400,
                'error_msg': ['ensure_new_password', 'new_password', 'reset_password_token']
            }
        }

        output = response.data
        output['error']['error_msg'] = extract_dict_keys(output['error']['error_msg'])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(expected_output, output)

    def test_absent_arguments_authorized(self):

        self.api_authentication()
        response = self.client.post(self.url, {})

        expected_output = {
            'ok': 0,
            'error': {
                'error_code': 400,
                'error_msg': ['ensure_new_password', 'new_password', 'old_password']
            }
        }

        output = response.data
        output['error']['error_msg'] = extract_dict_keys(output['error']['error_msg'])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(expected_output, output)


    def test_passwords_dont_match_anonymous(self):

        user_data = {
            'new_password': 'one',
            'ensure_new_password': 'two',
            'reset_password_token': 'token'
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ensure_new_password', response.data['error']['error_msg'].keys())

    def test_passwords_dont_match_authorized(self):

        self.api_authentication()

        user_data = {
            'new_password': 'one',
            'ensure_new_password': 'two',
            'old_password': self.password
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ensure_new_password', response.data['error']['error_msg'].keys())

    def test_invalid_reset_password_token_anonymous(self):

        _ = self.user.get_or_create_reset_password_token()

        user_data = {
            'new_password': 'password',
            'ensure_new_password': 'password',
            'reset_password_token': 'token'
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reset_password_token', response.data['error']['error_msg'].keys())

    def test_wrong_old_password_authorized(self):

        self.api_authentication()
        user_data = {
            'old_password': 'wrong',
            'new_password': 'newpass',
            'ensure_new_password': 'newpass'
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('old_password', response.data['error']['error_msg'].keys())

    def test_reset_password_token_expired_anonymous(self):

        token = self.user.get_or_create_reset_password_token()
        self.user._reset_password_token_valid_until = \
            self.user._reset_password_token_valid_until - timedelta(
                days=settings.RESET_PASSWORD_TOKEN_VALID_DAYS + 1)

        self.user.save()

        user_data = {
            'new_password': 'password',
            'ensure_new_password': 'password',
            'reset_password_token': token
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reset_password_token', response.data['error']['error_msg'].keys())

    def test_success_password_set_anonymous(self):

        token = self.user.get_or_create_reset_password_token()
        user_data = {
            'new_password': 'password_after',
            'ensure_new_password': 'password_after',
            'reset_password_token': token
        }

        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_success_password_set_authorized(self):

        self.api_authentication()
        user_data = {
            'old_password': self.password,
            'new_password': 'newpass',
            'ensure_new_password': 'newpass'
        }

        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_password_set_inside_model(self):

        self.user.set_password('new_password')
        self.assertTrue(self.user.check_password('new_password'))
        self.assertIsNone(self.user._reset_password_token)
        self.assertIsNone(self.user._reset_password_token_valid_until)


class ObtainResetTokenTestCase(APITestCase):

    url = reverse('obtain_reset_token')

    def setUp(self):

        self.username = 'qua_user'
        self.email = 'qua_user@gmail.com'
        self.password = 'qua_password'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = UserSession.objects.create(
            user=self.user,
            user_agent='',
            ip_address='').access_token

    def test_absent_input(self):

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(['email'], list(response.data['error']['error_msg'].keys()))

    def test_bad_email(self):

        user_data = {
            'email': 'bad_email'
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(['email'], list(response.data['error']['error_msg'].keys()))

    def test_nonexistent_email(self):

        user_data = {
            'email': 'man@gmail.com'
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(['email'], list(response.data['error']['error_msg'].keys()))

    def test_email_sent_with_token(self):

        user_data = {
            'email': self.email
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(mail.outbox), 1)

        reset_mail = mail.outbox[0]
        token = extract_token(reset_mail.body)

        self.assertEqual(reset_mail.subject, 'Сброс пароля в QUA')
        self.assertIsNotNone(token)


class ObtainAccessTokenTestCase(APITestCase):

    url = reverse('obtain_access_token')

    def setUp(self):

        self.username = 'qua_user'
        self.email = 'qua_user@gmail.com'
        self.password = 'qua_password'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_absent_input(self):

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data
        data['error']['error_msg'] = extract_dict_keys(
            data['error']['error_msg'])
        expected_output = {
            'ok': 0,
            'error': {
                'error_code': 400,
                'error_msg': ['password', 'username']
            }
        }

        self.assertEqual(data, expected_output)

    def test_incorrect_password(self):

        user_data = {
            'username': self.username,
            'password': 'wrong'
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        data = response.data
        data['error']['error_msg'] = extract_dict_keys(
            data['error']['error_msg'])
        expected_output = {
            'ok': 0,
            'error': {
                'error_code': 401,
                'error_msg': ['detail']
            }
        }

        self.assertEqual(data, expected_output)

    def test_success(self):

        user_data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        data['response'] = extract_dict_keys(data['response'])
        expected_output = {
            'ok': 1,
            'response': ['access_token']
        }

        self.assertEqual(data, expected_output)


class UserSessionsTestCase(APITestCase):

    url = reverse('user_sessions')

    def setUp(self):

        self.user = User.objects.create_user(
            'qua_user',
            'qua_user@gmail.com',
            'qua_password')
        self.session = UserSession.objects.create(
            user=self.user,
            user_agent='',
            ip_address='')

        UserSession.objects.create(
            user=self.user,
            user_agent='',
            ip_address='')

        self.api_authentication()

    def api_authentication(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.session.access_token)

    def test_session_list(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['response']), 2)

        one = response.data['response'][0]

        expected_fields = sorted(['browser', 'browser_version', 'created',
            'current', 'id', 'ip_address',
            'last_use', 'os', 'os_version', 'user_agent'])
        fields = extract_dict_keys(one)

        self.assertEqual(expected_fields, fields)

    def test_delete_all_sessions_except_current(self):

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_output = {
            'ok': 1,
            'response': {}
        }

        self.assertEqual(response.data, expected_output)

        response = self.client.get(self.url)

        self.assertEqual(len(response.data['response']), 1)

    def test_list_anonymous_user(self):

        self.client.credentials()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_anonymous_user(self):

        self.client.credentials()
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class IndividualUserSessionTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            'qua_user',
            'qua_user@gmail.com',
            'qua_password')
        self.session = UserSession.objects.create(
            user=self.user,
            user_agent='',
            ip_address='')

        UserSession.objects.create(
            user=self.user,
            user_agent='',
            ip_address='')

        self.api_authentication()

    def api_authentication(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.session.access_token)

    def get_url(self, session_id):

        return reverse(
            'individual_user_session',
            kwargs={'session_id': session_id})

    def test_not_authorized(self):

        self.client.credentials()

        url = self.get_url('current')
        response = self.client.delete(url, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_session_id(self):

        session_id = '123d'
        url = self.get_url(session_id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_output = {
            'ok': 0,
            'error': {
                'error_code': 400,
                'error_msg': ['session_id']
            }
        }

        data = response.data
        data['error']['error_msg'] = extract_dict_keys(
            data['error']['error_msg'])

        self.assertEqual(expected_output, data)

    def test_not_found_session(self):

        sessions = self.client.get(reverse('user_sessions')).data['response']
        session_ids = [sess['id'] for sess in sessions]

        absent_session_id = max(session_ids) + 1

        url = self.get_url(absent_session_id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data['error']['error_msg'])

    def test_delete_current_session(self):

        url = self.get_url('current')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_not_current_session(self):

        sessions = self.client.get(reverse('user_sessions')).data['response']
        not_current_session = [sess['id'] for sess in sessions if not sess['current']][0]
        url = self.get_url(not_current_session)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sessions = self.client.get(reverse('user_sessions')).data['response']
        session_types = [sess['current'] for sess in sessions]

        self.assertEqual(session_types, [True])
