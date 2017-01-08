from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.cache import cache
import markdown
from django.db.models.signals import post_save
from django.dispatch import receiver

from qua.api.utils import common
from qua.api import constants

import logging

log = logging.getLogger('qua.' + __name__)


class Categories(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return self.name


class Keywords(models.Model):
    text = models.CharField(max_length=50, unique=True)

    @classmethod
    @transaction.atomic
    def ensure_exists(cls, words):
        log.debug('Check all adding keywords exists')

        words = common.ensure_list(words)

        for i in range(len(words)):
            words[i] = common.word_normalize(words[i])

        try:
            exists = set(it.text for it in cls.objects.filter(text__in=words))
        except cls.DoesNotExist:
            exists = set()

        log.debug('Words: <%s> already exist', exists)

        for kw in set(words) - exists:
            cls.objects.create(text=kw)

        return cls.objects.filter(text__in=set(words) | exists)

    def __str__(self):
        return self.text


class Questions(models.Model):
    categories = models.ManyToManyField(Categories, blank=True)
    title = models.CharField(max_length=200)
    keywords = models.ManyToManyField(Keywords, blank=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return '<{0}:{1:.30}>'.format(self.id, self.title)

    def archive(self):
        self.deleted = True
        self.save()


class SearchHistory(models.Model):
    query = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    results = models.IntegerField()
    searched_at = models.DateTimeField(auto_now_add=True)
    clicked_at = models.DateTimeField(blank=True, null=True)
    question = models.ForeignKey(
        Questions, on_delete=models.PROTECT, related_name='+', blank=True, null=True)

    def __str__(self):
        return '({4}) <{0}:{1:.30}> -> {2} ({3})'.format(
            self.id, self.query, self.question, self.user, self.results)


class Answers(models.Model):
    raw = models.TextField()
    question = models.OneToOneField(
        Questions, related_name='answer', on_delete=models.CASCADE)
    snippet = models.CharField(max_length=200)
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return self.snippet

    @classmethod
    def create(cls, raw, user, question, snippet=None):
        if snippet is None:
            snippet = common.snippet(raw)
        answer = cls.objects.create(raw=raw, snippet=snippet,
            created_by=user, updated_by=user, question=question)

        return answer

    @property
    def name(self):
        return 'answer-%s' % self.id

    @property
    def html(self):
        html = cache.get(self.name)

        if html is None:
            html = cache.get_or_set(
                self.name, markdown.markdown(self.raw), constants.MONTH)

        return html


@receiver(post_save, sender=Answers)
def delete_cached_html(sender, **kwargs):
    cache.delete(kwargs['instance'].name)
