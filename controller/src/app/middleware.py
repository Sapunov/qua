'''
Copyright (c) 2018, QUA
Автор: Никита Сапунов
Описание: Промежуточные слои при обработке запроса пользователя
'''
import logging

from django.http import JsonResponse
from rest_framework import status

from app.common import get_logger
from app.rest import error_format


log = get_logger(__name__)


class ExceptionsHandlingMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        # rest_framework добавляет `data` к response,
        # поэтому этот код будет работать только тогда,
        # когда исключение возникло при маршрутизации
        if not hasattr(response, 'data') and \
                response.status_code == status.HTTP_404_NOT_FOUND:
            return JsonResponse(
                error_format(404, 'Endpoint not found =('),
                status=status.HTTP_404_NOT_FOUND)

        return response

    def process_exception(self, request, exception):

        log.exception(exception)

        return JsonResponse(
            error_format(500, 'Unexpected server error =('),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
