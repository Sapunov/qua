'''Interconnection methods for search microservice'''

import logging

from django.conf import settings
from rest_framework.exceptions import NotFound

from api import interconnect
from api import exceptions


log = logging.getLogger(settings.APP_NAME + __name__)


def index_item(
        ext_id, title, text, keywords=None, is_external=False, resource=None
):
    '''Send item data to the search service.
    Returns id of the item in search engine or False
    '''

    data = {
        'ext_id': ext_id,
        'title': title,
        'text': text,
        'is_external': is_external
    }

    if keywords:
        data['keywords'] = keywords

    if resource:
        data['resource'] = resource

    req = interconnect.post(
        'search.{0}/index'.format(settings.MAIN_SEARCH_SERVICE_NAME),
        json=data)

    if req.status_code == 200:
        return req.data['item_id']
    else:
        log.error('Cannot index question with search service: ' \
            'status_code: %s, response: %s', req.status_code, req.data)
        return False


def clear_index():
    '''Delete all items from search index'''

    req = interconnect.delete(
        'search.{0}/index'.format(settings.MAIN_SEARCH_SERVICE_NAME))

    if req.status_code == 200:
        return True
    else:
        log.error('Cannot clear search index: ' \
            'status_code: %s, response: %s', req.status_code, req.data)
        return False


def get_item(item_id):
    '''Returns search engine item specified by id'''

    req = interconnect.get(
        'search.{0}/items/{1}'.format(settings.MAIN_SEARCH_SERVICE_NAME, item_id))

    if req.status_code == 200:
        return req.data
    elif req.status_code == 404:
        return None
    else:
        log.error('Cannot get item with id: %s from search service: ' \
            'status_code: %s, response: %s', item_id, req.status_code, req.data)
        return False


def update_item(item_id, title=None, text=None, keywords=None, resource=None):
    '''Update search item via elasticsearch update call'''

    data = {}

    if title:
        data['title'] = title

    if text:
        data['text'] = text

    if keywords:
        data['keywords'] = keywords

    if resource:
        data['resource'] = resource

    req = interconnect.put(
        'search.{0}/items/{1}'.format(
            settings.MAIN_SEARCH_SERVICE_NAME, item_id), json=data)

    if req.status_code == 200:
        return True
    elif req.status_code == 404:
        raise NotFound('Item with id: %s does not found' % item_id)
    else:
        log.error('Cannot update item with id: %s within search service: ' \
            'status_code: %s, response: %s', item_id, req.status_code, req.data)
        return False


def delete_item(item_id):
    '''Delete item from search index'''

    req = interconnect.delete(
        'search.{0}/items/{1}'.format(settings.MAIN_SEARCH_SERVICE_NAME, item_id))

    if req.status_code == 200:
        return True
    elif req.status_code == 404:
        raise NotFound('Item with id: %s does not found' % item_id)
    else:
        log.error('Cannot delete item with id: %s from search service: ' \
            'status_code: %s, response: %s', item_id, req.status_code, req.data)
        return False
