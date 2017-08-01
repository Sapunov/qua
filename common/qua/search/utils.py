import logging
import lxml.html
import re

from qua import misc
from qua import settings as qua_settings
from qua.elasticsearch import get_client
from qua.search.stopwords import STOPWORDS


log = logging.getLogger(qua_settings.APP_NAME + '.' + __name__)


def create_boolean_query(queries, policy='should'):

    return {'bool': {policy: queries}}


def search_query(
        body,
        index=qua_settings.ES_SEARCH_INDEX,
        doc_type=qua_settings.ES_DOCTYPE,
        **kwargs
):

    client = get_client()

    if 'size' in kwargs and kwargs['size'] > qua_settings.MAX_SEARCH_RESULTS:
        kwargs['size'] = qua_settings.MAX_SEARCH_RESULTS
    elif 'size' not in kwargs:
        kwargs['size'] = qua_settings.MAX_SEARCH_RESULTS

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


def _html2text(node, forbidden_tags):

    children = node.getchildren()

    if children:
        text = ''
        for child in children:
            text += ' %s ' % _html2text(child, forbidden_tags)
        return text
    else:
        if node.tag not in forbidden_tags and \
                not isinstance(node, lxml.html.HtmlComment):
            return ' %s ' % node.text if node.text else ''
        else:
            return ''


def deduplicate_spaces(text):

    return re.sub('(\s)+', ' ', text).strip()


def html2text(html, forbidden_tags=['script', 'style', 'noscript', 'img']):

    tree = lxml.html.fromstring(html)
    title = tree.find(".//title")
    body = tree.find('.//body')

    if body is None or title is None:
        return ''

    return {
        'title': title.text,
        'text': deduplicate_spaces(_html2text(body, forbidden_tags))
    }


def generate_item_id(ext_id, is_external):
    '''Generate search engine internal id for item.'''

    return '{0}-{1}'.format(
        'e' if is_external else 'i', misc.int2hex_id(ext_id)
    )


def delete_stopwords(list_of_words):
    '''Delete words from list which defined as stopwords.'''

    return [word for word in list_of_words if not word in STOPWORDS]


def preprocess_user_query(user_query):
    '''Makes very first preprocessing.'''

    query = user_query.strip().lower()
    query_words = query.split(' ')
    meanful_words = delete_stopwords(query_words)

    return ' '.join(meanful_words)


def multimatch_builder(query, fields=qua_settings.SEARCH_FIELDS, operator='or'):
    '''Return dict with part of ES syntax for multimatch query.'''

    return {
        'multi_match': {
            'query': query,
            'fields': fields,
            'operator': operator
        }
    }


def delete_duplicates(list_of_items):
    '''Returns list with unique items of list_of_items.'''

    return list(set(list_of_items))


def highlight_words(string, word):
    '''Return string with word surrounded by <em> tags

    If word is None the whole string will be surrounded.
    '''

    if word is None:
        return '<em>{0}</em>'.format(string)

    words = string.split(' ')
    words[words.index(word)] = '<em>{0}</em>'.format(word)

    return ' '.join(words)
