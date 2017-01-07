from rest_framework.views import exception_handler

import logging

log = logging.getLogger('qua.' + __name__)


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
