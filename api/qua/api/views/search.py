import logging

from rest_framework import exceptions
from rest_framework.views import APIView
from django.conf import settings

from qua.api.search import search
from qua.api.response import QuaApiResponse
from qua.api.serializers import SearchSerializer
from qua.api.pagination import paginate


log = logging.getLogger('qua.' + __name__)


class SearchView(APIView):

    @paginate
    def get(self, request, format=None, limit=settings.PAGE_SIZE, offset=0):

        params = request.query_params

        if 'query' not in params:
            raise exceptions.ValidationError({'query': ['This field required']})

        if 'spelling' in params:
            spelling = (params['spelling'] == 1)
        else:
            spelling = True

        results = search.basesearch(
            params['query'],
            user=request.user,
            spelling=spelling,
            limit=limit,
            offset=offset
        )
        serializer = SearchSerializer(results)

        return QuaApiResponse(serializer.data)
