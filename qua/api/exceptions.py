from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

import logging

log = logging.getLogger('qua.' + __name__)


class QuaException(APIException):
    pass


def custom_api_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        log.debug('Exception: %s', response.data)

        response.data = {
            "ok": 0,
            "error": {
                "error_code": response.status_code,
                "error_msg": response.data
            }
        }

    return response


class ExitDecoratorError(QuaException):
    pass
