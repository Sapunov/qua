import logging

from django.conf import settings
from rest_framework.exceptions import NotFound

from search import elasticsearch
from search.engine import utils


esclient = elasticsearch.get_client()

log = logging.getLogger(settings.APP_NAME + '.' + __name__)


def add_to_spelling_db(*args):
    '''Add some text to the spelling index'''

    log.debug('Trying to add data in spelling index: %s', args)

    for data in args:
        if not isinstance(data, str):
            log.debug('Cannot add %s to the spelling index: not str', data)
            continue

        esclient.index(
            index=settings.ES_SPELLING_INDEX,
            doc_type=settings.ES_DOCTYPE,
            body={'text': data})

    log.debug('Items added to the spelling database')


def index_item(ext_id, title, text, keywords, is_external, resource):
    '''Save some item in ES database'''

    log.debug('Indexing question with ext_id=%s', ext_id)

    data = {
        'ext_id': ext_id,
        'title': title,
        'text': text,
        'keywords': keywords,
        'is_external': is_external,
        'resource': resource
    }

    log.debug('Data to store in database: %s', data)

    item_id = utils.generate_item_id(ext_id, is_external)

    log.debug('New item_id for item: %s', item_id)

    esclient.index(
        index=settings.ES_SEARCH_INDEX,
        doc_type=settings.ES_DOCTYPE,
        id=item_id,
        body=data)

    add_to_spelling_db(title, text, ' '.join(keywords))

    log.debug('Item with item_id=%s saved to index', item_id)

    return item_id


def get_item(item_id):
    '''Get es item by item_id'''

    log.debug('Trying to return item with item_id=%s', item_id)

    try:
        item = esclient.get(
            index=settings.ES_SEARCH_INDEX,
            doc_type=settings.ES_DOCTYPE,
            id=item_id)
    except elasticsearch.exceptions.NotFoundError:
        log.info('Item with item_id=%s not found!', item_id)
        raise NotFound

    item['_source']['item_id'] = item['_id']

    return item['_source']


def update_item(item_id, data):
    '''Update some item'''

    log.debug('Updating item with item_id=%s by data=%s', item_id, data)

    try:
        esclient.update(
            index=settings.ES_SEARCH_INDEX,
            doc_type=settings.ES_DOCTYPE,
            id=item_id,
            body={'doc': data})
    except elasticsearch.exceptions.NotFoundError:
        raise NotFound

    log.debug('Item with item_id=%s was updated', item_id)

    return get_item(item_id)


def delete_item(item_id):
    '''Delete item by item_id'''

    log.debug('Deleting item with item_id=%s', item_id)

    try:
        esclient.delete(
            index=settings.ES_SEARCH_INDEX,
            doc_type=settings.ES_DOCTYPE,
            id=item_id)
    except elasticsearch.exceptions.NotFoundError:
        log.info('Item with item_id=%s does not exist', item_id)


def clear_index():
    '''Clearing search index'''

    log.debug(
        'Clearing `%s` index with %s items',
        settings.ES_SEARCH_INDEX,
        esclient.count(
            index=settings.ES_SEARCH_INDEX,
            doc_type=settings.ES_DOCTYPE)['count'])

    esclient.delete_by_query(
        index=settings.ES_SEARCH_INDEX,
        doc_type=settings.ES_DOCTYPE,
        body={'query': {'match_all': {}}})
