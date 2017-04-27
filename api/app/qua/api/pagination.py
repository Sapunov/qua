import logging

from django.conf import settings
from rest_framework.utils.urls import remove_query_param, replace_query_param


log = logging.getLogger('qua.' + __name__)


LIMIT_QUERY_PARAM = 'limit'
OFFSET_QUERY_PARAM = 'offset'
DEFAULT_LIMIT = settings.PAGE_SIZE


def _positive_int(integer_string):

    integer = int(integer_string)

    if integer < 0:
        raise ValueError

    return integer


def _get_limit(request):

    params = request.query_params

    if LIMIT_QUERY_PARAM in params:
        try:
            return _positive_int(params[LIMIT_QUERY_PARAM])
        except (KeyError, ValueError):
            pass

    return DEFAULT_LIMIT


def _get_offset(request):

    params = request.query_params

    if OFFSET_QUERY_PARAM in params:
        try:
            return _positive_int(params[OFFSET_QUERY_PARAM])
        except (KeyError, ValueError):
            return 0

    return 0


def _get_next_link(request, limit, offset, total):

    if limit + offset >= total:
        return None

    url = request.get_full_path()
    url = replace_query_param(url, LIMIT_QUERY_PARAM, limit)

    offset = limit + offset

    return replace_query_param(url, OFFSET_QUERY_PARAM, offset)


def _get_previous_link(request, limit, offset):

    if offset <= 0:
        return None

    url = request.get_full_path()
    url = replace_query_param(url, LIMIT_QUERY_PARAM, limit)

    if offset - limit < 0:
        offset = 0
    else:
        offset = offset - limit

    return replace_query_param(url, OFFSET_QUERY_PARAM, offset)


def _add_pagination_content(request, response, limit, offset, total):

    log.debug('Limit: %s, offset: %s', limit, offset)

    pagination = {
        'next': _get_next_link(request, limit, offset, total),
        'prev': _get_previous_link(request, limit, offset)
    }

    response.data['response']['pagination'] = pagination

    return response


def paginate(func):

    def paginate_wrapper(self, request, *args, **kwargs):

        kwargs['limit'] = _get_limit(request)
        kwargs['offset'] = _get_offset(request)

        response = func(self, request, *args, **kwargs)

        if response.data['ok'] == 0:
            return response

        total = response.data['response']['total']

        return _add_pagination_content(
            request, response, kwargs['limit'], kwargs['offset'], total
        )

    return paginate_wrapper
