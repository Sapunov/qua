import elasticsearch
from elasticsearch import exceptions


def get_search_engine():

    return elasticsearch.Elasticsearch(
        timeout=30,
        max_retries=10,
        retry_on_timeout=True
    )
