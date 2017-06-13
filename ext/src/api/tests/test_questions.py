from django.contrib.auth.models import User
from django.test import tag

from api.models import Question
from api.tests.common import BaseQuaTestCase


@tag('questions')
class QuestionTest(BaseQuaTestCase):

    def setUp(self):

        super(QuestionTest, self).setUp()

        self.user = User.objects.get(username='test')
        self.client = self.create_authorized_client()

        question = Question.create('test_question_1', self.user)
        question1 = Question.create('test_question_2', self.user)

        self.qids = [question.id, question1.id]

        data = {
            'title': 'Full question',
            'keywords': ['hello', 'bro'],
            'answer': {'raw': 'Hello bro!'}
        }
        question2 = self.client.post('/questions', data, format='json').json()

        self.qids.append(question2['response']['id'])

    def test_format_list(self):

        resp = self.client.get('/questions')

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']
        items = response['items']

        self.assertEqual(len(response), 3)
        self.assertIn('total', response)
        self.assertIn('pagination', response)

        first = items[0]

        self.assertEqual(len(first.keys()), 8)

        self.assertIn('id', first)
        self.assertIn('title', first)
        self.assertIn('answer_exists', first)
        self.assertIn('keywords', first)
        self.assertIn('created_at', first)
        self.assertIn('updated_at', first)
        self.assertIn('created_by', first)
        self.assertIn('updated_by', first)

    def test_format_one(self):

        resp = self.client.get('/questions/' + str(self.qids[0]))

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']

        self.assertEqual(len(response.keys()), 9)

        self.assertIn('id', response)
        self.assertIn('title', response)
        self.assertIn('answer', response)
        self.assertIn('keywords', response)
        self.assertIn('created_at', response)
        self.assertIn('updated_at', response)
        self.assertIn('created_by', response)
        self.assertIn('updated_by', response)
        self.assertIn('answer_exists', response)

    def test_format_create(self):

        data = {
            'title': 'test_question',
            'keywords': ['one', 'two', 'three'],
            'answer': {'raw': 'test_answer'}
        }
        resp = self.client.post(
            '/questions', data, format='json')

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']

        self.assertEqual(len(response.keys()), 9)
        self.assertIn('id', response)
        self.assertIn('title', response)
        self.assertIn('answer', response)
        self.assertIn('keywords', response)
        self.assertIn('created_at', response)
        self.assertIn('updated_at', response)
        self.assertIn('created_by', response)
        self.assertIn('updated_by', response)
        self.assertIn('answer_exists', response)

        answer = response['answer']

        self.assertEqual(len(answer.keys()), 7)
        self.assertIn('html', answer)
        self.assertIn('raw', answer)
        self.assertIn('version', answer)
        self.assertIn('created_at', answer)
        self.assertIn('updated_at', answer)
        self.assertIn('created_by', answer)
        self.assertIn('updated_by', answer)

    def test_format_update(self):

        data = {
            'title': 'test_question',
            'keywords': ['one', 'two', 'three'],
            'answer': {'raw': 'test_answer'}
        }
        resp = self.client.put(
            '/questions/' + str(self.qids[0]),
            data,
            format='json')

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']

        self.assertEqual(len(response.keys()), 9)
        self.assertIn('id', response)
        self.assertIn('title', response)
        self.assertIn('answer', response)
        self.assertIn('keywords', response)
        self.assertIn('created_at', response)
        self.assertIn('updated_at', response)
        self.assertIn('created_by', response)
        self.assertIn('updated_by', response)
        self.assertIn('answer_exists', response)

    def test_format_delete(self):

        resp = self.client.delete('/questions/' + str(self.qids[1]))

        data = resp.data

        self.assertIn('ok', data)
        self.assertIn('response', data)
        self.assertEqual(data['response'], None)

    def test_not_found_get(self):

        resp = self.client.get('/questions/500')

        self.assertEqual(resp.status_code, 404)

    def test_create_without_something(self):

        resp = self.client.post('/questions', {})

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.data['error']['error_msg'],
            {'title': ['This field is required.']})

    def test_create_with_only_keywords(self):

        data = {
            'title': 'test_question',
            'keywords': ['one', 'two', 'three']
        }
        resp = self.client.post(
            '/questions', data, format='json')

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']

        self.assertEqual(len(response['keywords']), 3)
        self.assertEqual(response['answer'], None)

    def test_create_with_answer(self):

        data = {
            'title': 'test_question',
            'answer': {'raw': 'test_answer'}
        }
        resp = self.client.post(
            '/questions', data, format='json')

        self.assertEqual(resp.status_code, 200)

        response = resp.data['response']

        self.assertEqual(len(response['answer'].keys()), 7)
        self.assertEqual(response['keywords'], [])

    def test_update_empty(self):

        resp = self.client.put('/questions/' + str(self.qids[0]), {})

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.data['response'].keys()), 9)

    def test_update_keywords(self):

        first_keywords = ['one', 'two']
        second_keywords = ['two', 'three']

        data = {
            'title': 'test',
            'keywords': first_keywords
        }

        created = self.client.post(
            '/questions', data, format='json')

        created_id = created.data['response']['id']

        data_update = {
            'keywords': second_keywords
        }

        resp = self.client.put(
            '/questions/{0}'.format(created_id),
            data_update, format='json')

        self.assertEqual(resp.status_code, 200)

        keywords = Question.get(created_id).keywords.values_list(
            'text', flat=True)

        self.assertEqual(len(keywords), 2)
        self.assertIn('two', keywords)
        self.assertIn('three', keywords)

    def test_update_answer(self):

        client = self.create_authorized_client('test2', 'test2')
        data = {
            'answer': {
                'raw': 'Hello mother!'
            }
        }
        resp = client.put(
            '/questions/' + str(self.qids[2]), data, format='json')

        self.assertEqual(resp.status_code, 200)

        answer = resp.data['response']['answer']

        self.assertEqual(answer['raw'], 'Hello mother!')
        self.assertEqual(answer['version'], 2)
        self.assertEqual(answer['updated_by']['username'], 'test2')

    def test_update_answer_empty(self):

        data = {
            'answer': {
                'raw': ''
            }
        }
        resp = self.client.put(
            '/questions/' + str(self.qids[2]), data, format='json')

        self.assertEqual(resp.status_code, 200)

        answer = resp.data['response']['answer']

        self.assertIsNone(answer)

    def test_update_answer_same(self):

        client = self.create_authorized_client('test2', 'test2')
        data = {
            'answer': {'raw': 'Hello bro!'}
        }
        resp = client.put(
            '/questions/' + str(self.qids[2]), data, format='json')

        self.assertEqual(resp.status_code, 200)

        answer = resp.data['response']['answer']

        self.assertEqual(answer['version'], 1)
        self.assertEqual(answer['updated_by']['username'], 'test')

    def test_on_delete(self):

        self.client.delete('/questions/' + str(self.qids[1]))

        self.assertEqual(Question.objects.all().count(), 3)

        self.assertEqual(Question.objects.get(deleted=True).id, self.qids[1])
