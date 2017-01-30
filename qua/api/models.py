import logging
import mistune

from django.db import models
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.cache import cache
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


class Keyword(models.Model):

    text = models.CharField(max_length=50, primary_key=True)

    @classmethod
    def get_or_create(cls, words):
        """Return QuesrySet of keywords. Create if not exists

        :words: list (or one word) of words (not normalized)
        """
        if isinstance(words, str):
            words = [words]

        log.debug('Trying to retrieve keywords: %s', words)

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
    keywords = models.ManyToManyField(Keyword)
    deleted = models.BooleanField(default=False)
    # answer field in Answer

    def __str__(self):

        return '<Question: ({0}) {1:.30}>'.format(self.id, self.title)

    @classmethod
    def get(cls, pk=None, **kwargs):

        if pk is not None:
            try:
                return cls.objects.get(pk=pk, deleted=False, **kwargs)
            except cls.DoesNotExist:
                raise exceptions.NotFound

        results = cls.objects.filter(deleted=False, **kwargs)

        return results

    @classmethod
    def create(cls, title, user, keywords=None):

        log.debug('Creating question with title: %s, keywords: %s by %s',
            title, keywords, user
        )

        question = cls.objects.create(title=title, created_by=user, updated_by=user)

        log.debug('Created answer: %s', question)

        if keywords is not None:
            question.keywords = keywords

        question.save()

        return question

    def update(self, user, title=None, keywords=None):

        log.debug('Updating %s with title: %s, keywords: %s by %s',
            self, title, keywords, user
        )

        updates = 0

        if title is not None:
            self.title = title
            updates += 1

        if keywords is not None:
            self.keywords = keywords
            updates += 1

        log.debug('Found %s updates for %s. Saving...', updates, self)

        if updates > 0:
            self.updated_by = user
            self.save()

    def archive(self, user):

        log.debug('Archiving %s by %s', self, user)

        self.deleted = True
        self.save()

    def restore(self, user):

        log.debug('Restoring %s by %s', self, user)

        self.deleted = False
        self.save()

    @property
    def answer_exists(self):

        return hasattr(self, 'answer')

    class Meta:
        ordering = ('-answer', '-id')


class ExternalResource(Base):

    url = models.URLField(unique=True)

    @classmethod
    def create(cls, url, user):

        log.debug('Creating external resource: %s by %s', url, user)

        resource, _ = cls.objects.get_or_create(
            url=url, created_by=user, updated_by=user
        )

        log.debug('Created external resource is %s', resource.id)

        return resource

    def __str__(self):

        return self.url


class SearchHistory(models.Model):

    query = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    results = models.IntegerField()
    searched_at = models.DateTimeField(auto_now_add=True)
    clicked_at = models.DateTimeField(blank=True, null=True)
    question = models.ForeignKey(
        Question, on_delete=models.PROTECT, related_name='+', blank=True, null=True
    )
    external = models.BooleanField(default=False)
    external_resource = models.ForeignKey(
        ExternalResource, on_delete=models.PROTECT, related_name='+', blank=True, null=True
    )

    def __str__(self):
        return '({4}) <{0}:{1:.30}> -> {2} ({3})'.format(
            self.id, self.query, self.question, self.user, self.results)


class Answer(Base):

    raw = models.TextField()
    question = models.OneToOneField(
        Question, related_name='answer', on_delete=models.CASCADE
    )
    version = models.IntegerField(default=1)

    def __str__(self):

        return self.raw[0:50]

    @classmethod
    def create(cls, raw, user, question):

        if raw == '':
            return None

        log.debug('Creating answer with raw: %s for %s by %s', raw, question, user)

        answer = cls.objects.create(
            raw=raw, created_by=user, updated_by=user, question=question)

        log.debug('Created answer is %s', answer.name)

        return answer

    def update(self, raw, user):

        if self.raw != raw:
            log.debug('Updating <%s>', self.name)

            self.raw = raw
            self.version += 1
            self.updated_by = user

            self.save()

            cache.set(self.name, mistune.markdown(self.raw), constants.MONTH)

    def delete(self):

        log.debug('Deleting <%s>', self.name)

        cache.delete(self.name)
        super(Answer, self).delete()

    @property
    def name(self):

        return 'answer-%s' % self.id

    @property
    def html(self):

        html = cache.get(self.name)

        if html is None:
            log.debug('Compile markdown for <%s>', self.name)

            html = cache.get_or_set(
                self.name, mistune.markdown(self.raw), constants.MONTH)
        else:
            log.debug('Returning %s html from cache', self.name)

        return html
