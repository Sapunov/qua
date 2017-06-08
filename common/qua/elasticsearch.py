import logging

from elasticsearch import Elasticsearch as EsParent
from elasticsearch import exceptions

from qua import settings


log = logging.getLogger(settings.APP_NAME + __name__)

client = None


class Elasticsearch(EsParent):

    def __init__(self, *args, **kwargs):

        kwargs['hosts'] = kwargs.get('hosts', settings.ELASTICSEARCH['hosts'])
        kwargs['timeout'] = kwargs.get(
            'timeout', settings.ELASTICSEARCH['timeout']
        )
        kwargs['max_retries'] = kwargs.get(
            'max_retries', settings.ELASTICSEARCH['max_retries']
        )
        kwargs['retry_on_timeout'] = kwargs.get(
            'retry_on_timeout', settings.ELASTICSEARCH['retry_on_timeout']
        )

        super().__init__(*args, **kwargs)

    def search(self, *args, **kwargs):

        size = kwargs.get('size', None)
        if size is None or size > settings.MAX_SEARCH_RESULTS:
            kwargs['size'] = settings.MAX_SEARCH_RESULTS
        else:
            kwargs['size'] = size

        try:
            return super().search(*args, **kwargs)
        except exceptions.ElasticsearchException as e:
            log.exception('ElasticsearchException on search: %s', e)
            raise

    def index(self, *args, **kwargs):

        try:
            return super().index(*args, **kwargs)
        except exceptions.ElasticsearchException as e:
            log.exception('ElasticsearchException on index: %s', e)
            raise

    def get(self, *args, **kwargs):

        try:
            return super().get(*args, **kwargs)
        except exceptions.ElasticsearchException as e:
            log.exception('ElasticsearchException on get: %s', e)
            raise


def get_client(*args, **kwargs):

    global client

    if client is None:
        try:
            from django.conf import settings as app_settings
            from django.core.exceptions import ImproperlyConfigured

            if hasattr(app_settings, 'ES_HOSTS'):
                kwargs['hosts'] = kwargs.get('hosts', app_settings.ES_HOSTS)
        except (ImportError, ImproperlyConfigured):
            pass

        client = Elasticsearch(*args, **kwargs)
        log.debug('Created elasticsearch client %s', client)

    return client
