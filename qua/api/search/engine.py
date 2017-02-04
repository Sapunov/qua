import logging

import elasticsearch
from elasticsearch import exceptions


log = logging.getLogger('qua.' + __name__)


class SearchEngine(elasticsearch.Elasticsearch):

    def __init__(self, *args, **kwargs):

        kwargs['timeout'] = kwargs.get('timeout', 30)
        kwargs['max_retries'] = kwargs.get('max_retries', 10)
        kwargs['retry_on_timeout'] = kwargs.get('retry_on_timeout', True)

        super().__init__(*args, **kwargs)

    def search(self, *args, **kwargs):

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
