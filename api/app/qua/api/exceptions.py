import logging

from rest_framework.views import exception_handler
from rest_framework import exceptions as r_exceptions

from qua.api.utils.common import remove_empty_values


log = logging.getLogger('qua.' + __name__)


ONE_LAYER_EXCEPTIONS = ('detail', 'non_field_errors')


class QuaException(r_exceptions.APIException):
    pass


class ExitDecoratorError(QuaException):
    pass


def custom_api_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        log.debug('Status_code: %s, Exception: %s', response.status_code, response.data)

        response.data = remove_empty_values(response.data)

        if len(response.data) == 1:
            key = list(response.data.keys())[0]

            if key in ONE_LAYER_EXCEPTIONS:
                response.data = response.data[key]

            if isinstance(response.data, (list, tuple)) and len(response.data) == 1:
                response.data = response.data[0]

        response.data = {
            "ok": 0,
            "error": {
                "error_code": response.status_code,
                "error_msg": response.data
            }
        }

    return response
