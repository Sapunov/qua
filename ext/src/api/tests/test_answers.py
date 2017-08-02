from django.contrib.auth.models import User
from django.test import tag

from api.models import Answer, Question
from api.tests.common import BaseQuaTestCase


@tag('answers')
class AnswerTest(BaseQuaTestCase):

    def setUp(self):

        super(AnswerTest, self).setUp()

        self.user = User.objects.get(username='test')
        self.client = self.create_authorized_client()

        question = Question.objects.create(
            title='test_question_1',
            created_by=self.user,
            updated_by=self.user)

        self.qids = [question.id]

        Answer.create('test_raw_to_question_1', self.user, question)

        question2 = Question.objects.create(
            title='test_question_2',
            created_by=self.user,
            updated_by=self.user)

        self.qids.append(question2.id)

    def test_creating(self):

        q = Question.objects.get(pk=self.qids[1])
        answer = Answer.create('test_answer', self.user, q)

        self.assertEqual(answer.question.title, 'test_question_2')

    def test_markdown_works(self):

        resp = self.client.get('/questions/' + str(self.qids[0]))

        self.assertEqual(resp.status_code, 200)

        answer = resp.data['response']['answer']

        self.assertEqual(answer['html'], '<p>test_raw_to_question_1</p>\n')

    def test_update_html(self):

        resp_one = self.client.post(
            '/questions',
            {
                'title': 'hello',
                'answer': {'raw': 'test_answer_html'}
            },
            format='json'
        ).data['response']

        html_one = resp_one['answer']['html']

        resp_two = self.client.put(
            '/questions/%s' % resp_one['id'],
            {'answer': {'raw': '**test_answer_html_second**'}},
            format='json'
        ).data['response']

        html_two = resp_two['answer']['html']

        self.assertNotEqual(
            resp_one['answer']['raw'], resp_two['answer']['raw'])
        self.assertNotEqual(html_one, html_two)
