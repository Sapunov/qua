import json

from django.test import tag
from django.contrib.auth.models import User

from qua.api.tests.common import BaseQuaTestCase
from qua.api.models import Answer, Question


@tag('answers', 'ready')
class AnswerTest(BaseQuaTestCase):
    def setUp(self):
        super(AnswerTest, self).setUp()

        self.user = User.objects.get(pk=1)
        self.client = self.create_authorized_client()

        question = Question.objects.create(
            title='test_question_1', created_by=self.user, updated_by=self.user)
        Answer.create('test_raw_to_question_1', self.user, question)

        Question.objects.create(
            title='test_question_2', created_by=self.user, updated_by=self.user)

    def test_creating(self):
        q = Question.objects.get(pk=2)
        answer = Answer.create('test_answer', self.user, q)

        self.assertEqual(answer.question.title, 'test_question_2')

    def test_markdown_works(self):
        resp = self.client.get('/api/questions/1')

        self.assertEqual(resp.status_code, 200)

        answer = resp.data['response']['answer']

        self.assertEqual(answer['html'], '<p>test_raw_to_question_1</p>')

    def test_update_html(self):
        resp_one = self.client.post(
            '/api/questions',
            json.dumps({'title': 'hello', 'answer': {'raw': 'test_answer_html'}}),
            content_type='application/json'
        ).data['response']

        html_one = resp_one['answer']['html']

        resp_two = self.client.put(
            '/api/questions/%s' % resp_one['id'],
            json.dumps({'answer': {'raw': '**test_answer_html_second**'}}),
            content_type='application/json'
        ).data['response']

        html_two = resp_two['answer']['html']

        self.assertNotEqual(resp_one['answer']['raw'], resp_two['answer']['raw'])
        self.assertNotEqual(html_one, html_two)
