import json
import logging

from django.conf import settings
from rest_framework import exceptions
from rest_framework.views import APIView

from qua.api.pagination import paginate
from qua.api.response import QuaApiResponse


log = logging.getLogger('qua.' + __name__)


class SearchView(APIView):

    @paginate
    def get(self, request, format=None, limit=settings.PAGE_SIZE, offset=0):

        params = request.query_params

        if 'query' not in params:
            raise exceptions.ValidationError({'query': ['This field required']})

        # This is загрушка
        response = {
            'query': params['query'],
            'total': 0,
            'hits': [],
            'query_was_corrected': False,
            'used_query': params['query'],
            'took': 0
        }

        return QuaApiResponse(response)
