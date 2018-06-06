from django.conf import settings
from rest_framework import exceptions as r_exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from app.common import get_logger, expand_context_for_logging


log = get_logger(__name__)


def ok_format(ok=1, data=None):

    return {
        'ok': ok,
        'response': data
    }


def error_format(error_code, error_msg):

    return {
        'ok': 0,
        'error': {
            'error_code': error_code,
            'error_msg': error_msg
        }
    }


class QuaAPIResponse(Response):

    def __init__(self, data=None, **kwargs):

        super().__init__(data=ok_format(data=data), **kwargs)


class NotImplementedException(r_exceptions.APIException):

    status_code = status.HTTP_501_NOT_IMPLEMENTED
    default_detail = 'This method is not implemented'
    default_code = status.HTTP_501_NOT_IMPLEMENTED


def api_exception_handler(exception, context):

    log.debug('APIError: %s. Context: %s',
        exception, expand_context_for_logging(context))

    response = exception_handler(exception, context)

    if response is not None and isinstance(response.data, dict):
        response.data = error_format(response.status_code, response.data)

    return response
