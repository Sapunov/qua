import logging

from elasticsearch import Elasticsearch as EsParent
from elasticsearch import exceptions

from django.conf import settings


log = logging.getLogger(settings.APP_NAME + __name__)

client = None


class Elasticsearch(EsParent):
    '''DO NOT USE THIS CLASS DIRECTLY. USE `get_client` function!'''

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def search(self, *args, **kwargs):

        try:
            return super().search(*args, **kwargs)
        except exceptions.ElasticsearchException as exc:
            if not isinstance(exc, exceptions.NotFoundError):
                log.exception(exc)
            raise

    def index(self, *args, **kwargs):

        try:
            return super().index(*args, **kwargs)
        except exceptions.ElasticsearchException as exc:
            if not isinstance(exc, exceptions.NotFoundError):
                log.exception(exc)
            raise

    def get(self, *args, **kwargs):

        try:
            return super().get(*args, **kwargs)
        except exceptions.ElasticsearchException as exc:
            if not isinstance(exc, exceptions.NotFoundError):
                log.exception(exc)
            raise


def get_client(*args, **kwargs):

    global client

    if client is None:
        try:
            from django.core.exceptions import ImproperlyConfigured

            if hasattr(settings, 'ELASTICSEARCH'):
                kwargs['hosts'] = kwargs.get(
                    'hosts', settings.ELASTICSEARCH['hosts'])
        except ImproperlyConfigured:
            pass

        client = Elasticsearch(*args, **kwargs)

        log.debug('Elasticsearch client was created: %s', client)

    return client
