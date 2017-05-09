import lxml.html
import re

from qua import misc
from qua import settings
from qua.elasticsearch import get_client


def boolean_query(query_body, policy='should', query_type='match'):

    clause = []

    for key, values in query_body.items():
        if isinstance(values, (list, tuple, set)):
            for value in values:
                clause.append({
                    query_type: {
                        key: value
                    }
                })
        else:
            clause.append({
                query_type: {
                    key: values
                }
            })

    return {policy: clause}


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

    took = round(results['took'] / 1000, 3)
    total = results['hits']['total']

    if total > 0:
        out_results = [
            (res['_score'], res['_source']) for res in results['hits']['hits']
        ]
    else:
        out_results = None

    return (total, took, out_results)


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


def get_next_item_id():

    esclient = get_client()

    response = esclient.search(
        index=settings.ES_SEARCH_INDEX,
        doc_type=settings.ES_DOCTYPE,
        sort='_uid:desc',
        size=1)

    if response['hits']['total'] > 0:
        next_id = misc.int2hex_id(
            misc.hex_id2int(
                response['hits']['hits'][0]['_id']
            ) + 1
        )
    else:
        next_id = misc.int2hex_id(0)

    return next_id
