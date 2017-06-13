from django.test import tag
from django.contrib.auth.models import User

from api.tests.common import BaseQuaTestCase
from api.models import Keyword


@tag('keywords')
class KeywordTest(BaseQuaTestCase):

    def setUp(self):

        super(KeywordTest, self).setUp()

    def test_create_one_word(self):

        Keyword.get_or_create('first')

        keywords = Keyword.objects.all()

        self.assertEqual(keywords.count(), 1)
        self.assertEqual(keywords[0].text, 'first')

    def test_create_list(self):

        Keyword.get_or_create(['first', 'second'])

        keywords = Keyword.objects.values_list('text', flat=True)

        self.assertEqual(keywords.count(), 2)
        self.assertIn('first', keywords)
        self.assertIn('second', keywords)

    def test_return_type(self):

        keywords = Keyword.get_or_create(['first', 'second'])

        self.assertEqual(type(keywords), list)

    def test_return_num(self):

        keywords = Keyword.get_or_create(['first', 'second', 'third'])

        self.assertEqual(len(keywords), 3)

    def test_non_duplicate(self):

        Keyword.get_or_create(['first', 'second'])
        Keyword.get_or_create(['second', 'third'])
        Keyword.get_or_create(['second', 'first'])

        keywords = Keyword.objects.values_list('text', flat=True)

        self.assertEqual(len(keywords), 3)

        self.assertIn('first', keywords)
        self.assertIn('second', keywords)
        self.assertIn('third', keywords)

    def test_normalization(self):

        words = ['MaMa', 'G@zgolder', 'w0rD,.', ' peacE and wAr', 'mama-papa ']

        Keyword.get_or_create(words)
        keywords = Keyword.objects.values_list('text', flat=True)

        self.assertEqual(len(keywords), 5)

        self.assertIn('mama', keywords)
        self.assertIn('g@zgolder', keywords)
        self.assertIn('w0rd,.', keywords)
        self.assertIn('peace and war', keywords)
        self.assertIn('mama-papa', keywords)
