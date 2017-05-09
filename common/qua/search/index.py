import logging

from django.conf import settings

from qua import elasticsearch
from qua import settings as qua_settings
from qua.search import utils


esclient = elasticsearch.get_client()

log = logging.getLogger(settings.APP_NAME + __name__)


def add_to_spelling_db(*args):

    for data in args:
        if not isinstance(data, str):
            continue

        esclient.index(
            index=qua_settings.ES_SPELLING_INDEX,
            doc_type=qua_settings.ES_DOCTYPE,
            body={'text': data})

    log.debug('Items added to the spelling database')


def index_item(ext_id, title, text, keywords, is_external, resource):

    log.debug('Indexing question with ext_id=%s', ext_id)

    data = {
        'ext_id': ext_id,
        'title': title,
        'text': text,
        'keywords': keywords,
        'is_external': is_external,
        'resource': resource
    }

    item_id = utils.get_next_item_id()

    esclient.index(
        index=qua_settings.ES_SEARCH_INDEX,
        doc_type=qua_settings.ES_DOCTYPE,
        id=item_id,
        body=data)

    add_to_spelling_db(title, text, ' '.join(keywords))

    log.debug('New index item with item_id=%s', item_id)

    return item_id


def delete_item(item_id):

    log.debug('Deleting item with item_id=%s', item_id)

    try:
        esclient.delete(
            index=qua_settings.ES_SEARCH_INDEX,
            doc_type=qua_settings.ES_DOCTYPE,
            id=item_id)
    except elasticsearch.exceptions.NotFoundError:
        log.info('Item with item_id=%s does not exist', item_id)


def clear_index():

    log.debug(
        'Clearing `%s` index with %s items',
        qua_settings.ES_SEARCH_INDEX,
        esclient.count(
            index=qua_settings.ES_SEARCH_INDEX,
            doc_type=qua_settings.ES_DOCTYPE)['count'])

    esclient.delete_by_query(
        index=qua_settings.ES_SEARCH_INDEX,
        doc_type=qua_settings.ES_DOCTYPE,
        body={'query': {'match_all': {}}})
