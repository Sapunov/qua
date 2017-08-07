import logging
import mistune

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from rest_framework import exceptions
import datetime
import django_rq

from api import constants
from api import misc
from api import retriever
from api import search
from api import tasks


log = logging.getLogger(settings.APP_NAME + __name__)
queue = django_rq.get_queue(settings.APP_NAME)


class Base(models.Model):
    '''Base abstract class with common fields'''

    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='+', blank=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='+', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


class Keyword(models.Model):
    '''Qua keywords'''

    text = models.CharField(max_length=50, primary_key=True)

    @classmethod
    def get_or_create(cls, words):
        '''Return QuesrySet of keywords. Create if not exists

        :words: list (or one word) of words (not normalized)
        '''
        if isinstance(words, str):
            words = [words]

        log.debug('Trying to retrieve keywords: %s', words)

        keywords = []

        for word in words:
            normalized_word = misc.word_normalize(word)

            keyword, _ = cls.objects.get_or_create(pk=normalized_word)

            keywords.append(keyword)

        return keywords

    def __str__(self):

        return self.text


class QuestionListRepr:
    '''Helpful class for simplify pagination logic'''

    def __init__(self, queryset, total):

        self.items = queryset
        self.total = total


class Question(Base):
    '''Qua question'''

    title = models.CharField(max_length=300)
    keywords = models.ManyToManyField(Keyword)
    deleted = models.BooleanField(default=False)
    se_id = models.CharField(max_length=10, blank=True, null=True)
    # answer field in Answer

    def __str__(self):

        return '<Question: ({0}) {1:.30}>'.format(self.id, self.title)

    @classmethod
    def get(cls, pk=None, **kwargs):
        '''Returns list of questions or specific question'''

        offset = kwargs.pop('offset', 0)
        limit = kwargs.pop('limit', None)

        if pk is not None:
            try:
                return cls.objects.get(pk=pk, deleted=False, **kwargs)
            except cls.DoesNotExist:
                raise exceptions.NotFound

        results = cls.objects.filter(deleted=False, **kwargs)

        total = results.count()
        limit = limit if limit is not None else total

        return QuestionListRepr(results[offset:offset + limit], total)

    @classmethod
    def create(cls, title, user, keywords=None):
        '''Create question without creating answer'''

        log.debug(
            'Creating question with title: %s, keywords: %s by %s',
            title, keywords, user)

        question = cls.objects.create(
            title=title, created_by=user, updated_by=user)

        log.debug('Created answer: %s', question)

        if keywords is not None:
            question.keywords = keywords

        question.save()

        return question

    def update(self, user, title=None, keywords=None):
        '''Update specific question fields'''

        log.debug(
            'Updating %s with title: %s, keywords: %s by %s',
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
        '''Check deleted flag. Using when user delete question'''

        log.debug('Archiving %s by %s', self, user)

        self.deleted = True
        self.save()

        # delete from search index
        queue.enqueue(tasks.delete_from_index, self)

    def restore(self, user):
        '''Check off deleted flag'''

        log.debug('Restoring %s by %s', self, user)

        self.deleted = False
        self.save()

        # index question to make in searchable
        queue.enqueue(tasks.index_question, self)

    @property
    def answer_exists(self):
        '''Returns whether answer of this question exists'''

        return hasattr(self, 'answer')

    def get_keywords_text_only(self):
        '''Returns queryset of question keywords in text format'''

        return list(self.keywords.values_list('text', flat=True))

    class Meta:

        ordering = ('-answer', '-id')


class ExternalResource(Base):
    '''Qua external resourse'''

    scheme = models.CharField(max_length=10)
    hostname = models.URLField()
    update_interval = models.IntegerField(default=1)
    se_id = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=1000)
    _content_hash = models.CharField(max_length=40, default='')
    _url = models.URLField(unique=True)

    @classmethod
    def create(cls, url, user=None):
        '''Create external resource'''

        url = misc.normalize_url(url)

        hostname = misc.extract_hostname(url)
        scheme, url = misc.urlsep(url)

        resource, created = cls.objects.get_or_create(
            scheme=scheme,
            hostname=hostname,
            _url=url,
            created_by=user,
            updated_by=user)

        return resource, created

    @property
    def url(self):
        '''Concat scheme and _url and returns good url address'''

        return '{0}://{1}'.format(self.scheme, self._url)

    @property
    def need_update(self):
        '''Return whether this resource need to be updated'''

        now = timezone.now()
        interval = datetime.timedelta(days=self.update_interval)

        return self.updated_at + interval <= now

    def index_resource(self):
        '''Index external resource with search service'''

        html = retriever.retrieve_url(self.url)

        log.debug('HTML for updating %s: %s', self, misc.truncate_string(html))

        if not html:
            return False

        html_hash = misc.sha1_hash(html)
        title_text = misc.html2text(html)

        # index if it never indexed
        if self.se_id is None:
            item_id = search.index_item(
                self.id,
                title_text['title'],
                title_text['text'],
                is_external=True,
                resource=self.url)

            log.debug('Index %s for the first time. Search engine id=%s',
                      self, item_id)

            self.se_id = item_id
            self.title = title_text['title']
            self._content_hash = html_hash
        elif self._content_hash != html_hash:
            log.debug('Update %s because of new content', self)
            search.update_item(
                self.se_id,
                title=title_text['title'],
                text=title_text['text'])

            self._content_hash = html_hash
        elif self.update_interval < settings.MAX_UPDATE_INTERVAL:
            self.update_interval += 1
            log.debug('No new content for %s. Setting update_interval to %s',
                      self, self.update_interval)

        self.save()

        return True

    def __str__(self):

        return '<ExternalResource: ({0}) {1}>'.format(self.id, self.url)


class SearchHistory(models.Model):
    '''Qua search history'''

    query = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    results = models.IntegerField()
    searched_at = models.DateTimeField(auto_now_add=True)
    clicked_at = models.DateTimeField(blank=True, null=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True)
    external = models.BooleanField(default=False)
    external_resource = models.ForeignKey(
        ExternalResource,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True)

    def __str__(self):

        return '({4}) <{0}:{1:.30}> -> {2} ({3})'.format(
            self.id, self.query, self.question, self.user, self.results)


class Answer(Base):
    '''Qua question answer'''

    raw = models.TextField()
    question = models.OneToOneField(
        Question, related_name='answer',
        on_delete=models.CASCADE)
    version = models.IntegerField(default=1)

    def __str__(self):

        return self.raw[0:50]

    @classmethod
    def create(cls, raw, user, question):
        '''Create answer for a specific question'''

        if raw == '':
            return None

        log.debug(
            'Creating answer with raw: %s for %s by %s', raw, question, user)

        answer = cls.objects.create(
            raw=raw, created_by=user, updated_by=user, question=question)

        log.debug('Created answer is %s', answer.name)

        return answer

    def update(self, raw, user):
        '''Update specific answer'''

        if self.raw != raw:
            log.debug('Updating <%s>', self.name)

            self.raw = raw
            self.version += 1
            self.updated_by = user

            self.save()

            cache.set(self.name, mistune.markdown(self.raw), constants.MONTH)

    def delete(self):
        '''Delete specific answer'''

        log.debug('Deleting <%s>', self.name)

        cache.delete(self.name)
        super(Answer, self).delete()

    @property
    def name(self):
        '''Answer name with id'''

        return 'answer-%s' % self.id

    @property
    def html(self):
        '''Returns compiled html from markdown'''

        html = cache.get(self.name)

        if html is None:
            log.debug('Compile markdown for <%s>', self.name)

            html = cache.get_or_set(
                self.name, mistune.markdown(self.raw), constants.MONTH)
        else:
            log.debug('Returning %s html from cache', self.name)

        return html


class ExternalResourceSettings(models.Model):
    '''Settings of user specified external resources'''

    scheme = models.CharField(max_length=10)
    hostname = models.URLField(unique=True)
    _login = models.BinaryField(blank=True, null=True)
    _password = models.BinaryField(blank=True, null=True)

    @classmethod
    def create(cls, hostname, scheme='http', login=None, password=None):
        '''Create new resource with the specific settings'''

        if login is not None and password is not None:
            login = misc.aes_encrypt(login)
            password = misc.aes_encrypt(password)

        obj = cls.objects.create(
            scheme=scheme,
            hostname=hostname,
            _login=login,
            _password=password)

        return obj

    @property
    def login(self):
        '''Returns decrypted login'''

        if isinstance(self._login, memoryview):
            login = self._login.tobytes()
        else:
            login = self._login

        return misc.aes_decrypt(login)

    @login.setter
    def login(self, new_login):

        self._login = misc.aes_encrypt(new_login)
        self.save()

    @property
    def password(self):
        '''Returns decrypted password'''

        if isinstance(self._password, memoryview):
            password = self._password.tobytes()
        else:
            password = self._password

        return misc.aes_decrypt(password)

    @password.setter
    def password(self, new_password):

        self._password = misc.aes_encrypt(new_password)
        self.save()

    def __str__(self):

        return '<ExternalResourceSettings: ({0}) {1}>'.format(self.id, self.hostname)
