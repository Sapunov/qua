import logging
import lxml.html
import re

from qua import misc
from qua import settings
from qua.elasticsearch import get_client


log = logging.getLogger(settings.APP_NAME + '.' + __name__)


def boolean_query(queries, policy='should'):

    return {'bool': {policy: queries}}


def query(index, doc_type, body, **kwargs):

    client = get_client()

    if 'size' in kwargs and kwargs['size'] > settings.MAX_SEARCH_RESULTS:
        kwargs['size'] = settings.MAX_SEARCH_RESULTS
    elif 'size' not in kwargs:
        kwargs['size'] = settings.MAX_SEARCH_RESULTS

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

    return '{0}-{1}'.format(
        'e' if is_external else 'i', misc.int2hex_id(ext_id))
