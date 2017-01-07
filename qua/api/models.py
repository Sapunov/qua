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
        return self.title

    def archive(self):
        self.deleted = True
        self.save()

    def search(self, query, category=None):
        pass


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


class SearchHit:
    id = None
    title = None
    snippet = None
    image = None
    score = None
    category = None


class CategoryAssumptions:
    assumptions = None


class SearchResults:
    def __init__(self, query, hits, category_assumptions=None):
        self.query = query
        self.hits = hits
        self.total = len(hits)
        self.category_assumptions = category_assumptions
