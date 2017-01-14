import logging
import markdown

from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import exceptions

from qua.api.utils import common
from qua.api import constants


log = logging.getLogger('qua.' + __name__)


class Base(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Base):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '<Category: ({0}) {1}>'.format(self.id, self.name)

    @classmethod
    def create(cls, name, user):
        return cls.objects.create(name=name, created_by=user, updated_by=user)

    @classmethod
    def exists(cls, category):
        """Check whether category(s) exists

        :category: list of primary keys
        """
        if isinstance(category, list):
            return cls.objects.filter(pk__in=category).count() == len(category)
        else:
            return cls.objects.filter(pk=category).exists()


class Keyword(models.Model):
    text = models.CharField(max_length=50, primary_key=True)

    @classmethod
    def get_or_create(cls, words):
        """Return QuesrySet of keywords. Create if not exists

        :words: list (or one word) of words (not normalized)
        """
        if isinstance(words, str):
            words = [words]

        keywords = []

        for word in words:
            normalized_word = common.word_normalize(word)

            keyword, _ = cls.objects.get_or_create(pk=normalized_word)

            keywords.append(keyword)

        return keywords

    def __str__(self):
        return self.text


class Question(Base):
    title = models.CharField(max_length=300)
    categories = models.ManyToManyField(Category)
    keywords = models.ManyToManyField(Keyword)
    deleted = models.BooleanField(default=False)
    reindex = models.BooleanField(default=True)
    # answer field in Answer

    def __str__(self):
        return '<Question: ({0}) {1:.30}>'.format(self.id, self.title)

    @classmethod
    def get(cls, pk=None, category=None, **kwargs):
        if pk is not None:
            try:
                return cls.objects.get(pk=pk, deleted=False, **kwargs)
            except cls.DoesNotExist:
                raise exceptions.NotFound

        results = cls.objects.filter(deleted=False, **kwargs)

        if category is not None:
            results = results.filter(categories=category)

        return results

    @classmethod
    def create(cls, title, user, keywords=None, category_ids=None):
        question = cls.objects.create(title=title, created_by=user, updated_by=user)

        if keywords is not None:
            question.keywords = keywords

        if category_ids is not None:
            question.categories = Category.objects.filter(pk__in=category_ids)

        question.save()

        return question

    def update(self, user, title=None, keywords=None, category_ids=None):
        updates = 0

        if title is not None:
            self.title = title
            updates += 1

        if keywords is not None:
            self.keywords = keywords
            updates += 1

        if category_ids is not None:
            self.categories = Category.objects.filter(pk__in=category_ids)
            updates += 1

        if updates > 0:
            self.updated_by = user
            self.save()

    def archive(self):
        self.deleted = True
        self.save()

    def restore(self):
        self.deleted = False
        self.save()

    @property
    def answer_exists(self):
        return hasattr(self, 'answer')


class SearchHistory(models.Model):
    query = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    results = models.IntegerField()
    searched_at = models.DateTimeField(auto_now_add=True)
    clicked_at = models.DateTimeField(blank=True, null=True)
    question = models.ForeignKey(
        Question, on_delete=models.PROTECT, related_name='+', blank=True, null=True)

    def __str__(self):
        return '({4}) <{0}:{1:.30}> -> {2} ({3})'.format(
            self.id, self.query, self.question, self.user, self.results)


class Answer(Base):
    raw = models.TextField()
    question = models.OneToOneField(
        Question, related_name='answer', on_delete=models.CASCADE)

    version = models.IntegerField(default=1)

    def __str__(self):
        return self.raw[0:50]

    @classmethod
    def create(cls, raw, user, question):
        if raw == '':
            return None

        answer = cls.objects.create(
            raw=raw, created_by=user, updated_by=user, question=question)

        return answer

    def update(self, raw, user):
        if self.raw != raw:
            self.raw = raw
            self.version += 1
            self.updated_by = user

            self.save()

            cache.set(self.name, markdown.markdown(self.raw), constants.MONTH)

    @property
    def name(self):
        return 'answer-%s' % self.id

    @property
    def html(self):
        html = cache.get(self.name)

        if html is None:
            log.debug('Regenerating markdown. Raw: %s', self.raw)

            html = cache.get_or_set(
                self.name, markdown.markdown(self.raw), constants.MONTH)

        return html
