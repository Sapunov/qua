import json

from django.test import tag
from django.contrib.auth.models import User

from qua.api.tests.common import BaseQuaTestCase
from qua.api.models import Category


@tag('categories', 'ready')
class CategoryTest(BaseQuaTestCase):
    def setUp(self):
        super(CategoryTest, self).setUp()

        self.user = User.objects.get(pk=1)
        self.client = self.create_authorized_client()

        Category.create('Test category 1', self.user)
        Category.create('Test category 2', self.user)

    def test_list_all_categories(self):
        resp = self.client.get('/api/categories')

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']

        self.assertEqual(len(response), 2)

        first_item = response[0]
        second_item = response[1]

        self.assertEqual(first_item['id'], 1)
        self.assertEqual(second_item['id'], 2)

        self.assertEqual(first_item['name'], 'Test category 1')

        self.assertEqual(first_item['created_by']['username'], 'test')
        self.assertEqual(first_item['updated_by']['username'], 'test')

    def test_one_category(self):
        resp = self.client.get('/api/categories/2')

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']

        self.assertEqual(response['name'], 'Test category 2')

    def test_not_found_category(self):
        resp = self.client.get('/api/categories/3')

        self.assertEqual(resp.status_code, 404)

    def test_create_new_category(self):
        resp = self.client.post('/api/categories', {'name': 'created_category'})

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']
        self.assertEqual(response['name'], 'created_category')

        category = Category.objects.get(pk=3)

        self.assertEqual(category.name, 'created_category')

    def test_update_category(self):
        self.client.post('/api/categories', {'name': 'created_category'})

        resp = self.client.put('/api/categories/3',
            json.dumps({'name': 'updated_category'}),
            content_type='application/json')

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']
        self.assertEqual(response['name'], 'updated_category')

        category = Category.objects.get(pk=3)

        self.assertEqual(category.name, 'updated_category')

    def test_delete_category(self):
        self.client.post('/api/categories', {'name': 'created_category'})

        resp = self.client.delete('/api/categories/3')

        self.assertEqual(resp.status_code, 200)

        self.assertRaises(Category.DoesNotExist, Category.objects.get, pk=3)

    def test_update_on_empty_name(self):
        data = json.dumps({'name': ''})
        resp = self.client.put(
            '/api/categories/2', data, content_type='application/json')

        self.assertEqual(resp.status_code, 400)

        error = resp.data['error']

        self.assertEqual(error['error_msg'], {'name': ['This field may not be blank.']})

    def test_create_on_empty_name(self):
        data = json.dumps({'name': ''})
        resp = self.client.post(
            '/api/categories', data, content_type='application/json')

        self.assertEqual(resp.status_code, 400)

        error = resp.data['error']

        self.assertEqual(error['error_msg'], {'name': ['This field may not be blank.']})

    def test_create_without_name(self):
        resp = self.client.post(
            '/api/categories', '{}', content_type='application/json')

        self.assertEqual(resp.status_code, 400)

        error = resp.data['error']

        self.assertEqual(error['error_msg'], {'name': ['This field is required.']})

    def test_update_without_name(self):
        resp = self.client.put(
            '/api/categories/1', '{}', content_type='application/json')

        self.assertEqual(resp.status_code, 400)

        error = resp.data['error']

        self.assertEqual(error['error_msg'], {'name': ['This field is required.']})

    def test_update_by_another_user(self):
        client = self.create_authorized_client(username='test2', password='test2')
        data = json.dumps({'name': 'Hello bro'})
        resp = client.put(
            '/api/categories/2', data, content_type='application/json')

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']

        self.assertEqual(response['updated_by']['username'], 'test2')

    def test_format_list_categories(self):
        resp = self.client.get('/api/categories')
        response = resp.data['response']

        first = response[0]

        self.assertIn('id', first)
        self.assertIn('name', first)
        self.assertIn('created_by', first)
        self.assertIn('updated_by', first)
        self.assertIn('created_at', first)
        self.assertIn('updated_at', first)

        self.assertEqual(len(first.keys()), 6)

    def test_format_one_category(self):
        resp = self.client.get('/api/categories/1')
        response = resp.data['response']

        self.assertIn('id', response)
        self.assertIn('name', response)
        self.assertIn('created_by', response)
        self.assertIn('updated_by', response)
        self.assertIn('created_at', response)
        self.assertIn('updated_at', response)

        self.assertEqual(len(response.keys()), 6)

    def test_format_update_category(self):
        data = json.dumps({'name': 'Hello bro'})
        resp = self.client.put(
            '/api/categories/1', data, content_type='application/json')
        response = resp.data['response']

        self.assertIn('id', response)
        self.assertIn('name', response)
        self.assertIn('created_by', response)
        self.assertIn('updated_by', response)
        self.assertIn('created_at', response)
        self.assertIn('updated_at', response)

        self.assertEqual(len(response.keys()), 6)

    def test_format_create_category(self):
        data = json.dumps({'name': 'Hello bro'})
        resp = self.client.post(
            '/api/categories', data, content_type='application/json')
        response = resp.data['response']

        self.assertIn('id', response)
        self.assertIn('name', response)
        self.assertIn('created_by', response)
        self.assertIn('updated_by', response)
        self.assertIn('created_at', response)
        self.assertIn('updated_at', response)

        self.assertEqual(len(response.keys()), 6)

    def test_format_delete_category(self):
        resp = self.client.delete('/api/categories/2')

        data = resp.data

        self.assertIn('ok', data)
        self.assertIn('response', data)
        self.assertEqual(data['response'], None)
