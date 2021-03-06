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


def highlight_words(query_terms, highlight_all=False):
    '''Return string with word surrounded by <em> tags

    If word is None the whole string will be surrounded.
    '''

    format_str = '<em>{0}</em>'

    if highlight_all:
        return format_str.format(' '.join(term[0] for term in query_terms))

    words = []
    for user_term, suggested_term in query_terms:
        if suggested_term is not None:
            words.append(format_str.format(suggested_term))
        else:
            words.append(user_term)

    return ' '.join(words)


def string2terms(string):
    '''Create query terms from string split it by space'''

    query_terms = []

    for word in string.split(' '):
        query_terms.append((word, None))

    return query_terms
