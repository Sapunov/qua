import logging

from django.conf import settings
from rest_framework import exceptions as r_exceptions
from rest_framework.views import exception_handler


log = logging.getLogger(settings.APP_NAME + __name__)


ONE_LAYER_EXCEPTIONS = ('detail', 'non_field_errors')


class QuaException(r_exceptions.APIException):

    pass


class ExitDecoratorError(QuaException):

    pass


def _remove_empty_values(data):

    if isinstance(data, dict):
        clear_dict = {}

        for key, value in data.items():
            cleared_value = _remove_empty_values(value)
            if cleared_value:
                clear_dict[key] = cleared_value

        return clear_dict
    elif isinstance(data, list):
        clear_list = []

        for item in data:
            cleared_value = _remove_empty_values(item)
            if cleared_value:
                clear_list.append(cleared_value)

        return clear_list
    else:
        return data if data else False


def api_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        log.debug(
            'Status_code: %s, Exception: %s',
            response.status_code,
            response.data)

        response.data = _remove_empty_values(response.data)

        if len(response.data) == 1:
            key = list(response.data.keys())[0]

            if key in ONE_LAYER_EXCEPTIONS:
                response.data = response.data[key]

            if isinstance(response.data, (list, tuple)) \
                    and len(response.data) == 1:
                response.data = response.data[0]

        response.data = {
            "ok": 0,
            "error": {
                "error_code": response.status_code,
                "error_msg": response.data
            }
        }

    return response
