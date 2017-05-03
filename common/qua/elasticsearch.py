from elasticsearch import Elasticsearch as EsParent
from elasticsearch import exceptions

from qua import settings


class Elasticsearch(EsParent):

    def __init__(self, *args, **kwargs):

        kwargs['hosts'] = settings.ELASTICSEARCH['hosts']
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
            # log.exception('ElasticsearchException on search: %s', e)
            raise

    def index(self, *args, **kwargs):
        try:
            return super().index(*args, **kwargs)
        except exceptions.ElasticsearchException as e:
            # log.exception('ElasticsearchException on index: %s', e)
            raise

    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except exceptions.ElasticsearchException as e:
            # log.exception('ElasticsearchException on get: %s', e)
            raise
