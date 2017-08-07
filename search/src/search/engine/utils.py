import lxml.html
import re

from django.conf import settings

from search import elasticsearch
from search import misc
from search.engine import stopwords


def create_boolean_query(queries, policy='should'):
    '''Return ES specific formed dict for boolean query'''

    return {'bool': {policy: queries}}


def search_query(
        body,
        index=settings.ES_SEARCH_INDEX,
        doc_type=settings.ES_DOCTYPE,
        **kwargs
):

    client = elasticsearch.get_client()

    results = client.search(
        index=index,
        doc_type=doc_type,
        body=body, **kwargs)

    total = results['hits']['total']
    out_results = []

    if total > 0:
        for res in results['hits']['hits']:
            out_results.append((res['_score'], res['_id'], res['_source']))

    return (total, results['took'], out_results)


def generate_item_id(ext_id, is_external):
    '''Generate search engine internal id for item.'''

    return '{0}-{1}'.format(
        'e' if is_external else 'i', misc.int2hex_id(ext_id)
    )


def delete_stopwords(list_of_words):
    '''Delete words from list which defined as stopwords.'''

    return [word for word in list_of_words if not word in stopwords.STOPWORDS]


def preprocess_user_query(user_query):
    '''Makes very first preprocessing.'''

    query = user_query.strip().lower()
    query_words = query.split(' ')
    meanful_words = delete_stopwords(query_words)

    return ' '.join(meanful_words)


def multimatch_builder(query, fields=settings.ES_SEARCH_FIELDS, operator='or'):
    '''Return dict with part of ES syntax for multimatch query.'''

    return {
        'multi_match': {
            'query': query,
            'fields': fields,
            'operator': operator
        }
    }


def highlight_words(string, word):
    '''Return string with word surrounded by <em> tags

    If word is None the whole string will be surrounded.
    '''

    if word is None:
        return '<em>{0}</em>'.format(string)

    words = string.split(' ')
    words[words.index(word)] = '<em>{0}</em>'.format(word)

    return ' '.join(words)
