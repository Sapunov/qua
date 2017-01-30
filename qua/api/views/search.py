import logging

from rest_framework import exceptions
from rest_framework.views import APIView

from qua.api.search import search
from qua.api.response import QuaApiResponse
from qua.api.serializers import SearchSerializer


log = logging.getLogger('qua.' + __name__)


class SearchView(APIView):

    def get(self, request, format=None):
        params = request.query_params

        if 'query' not in params:
            raise exceptions.ValidationError({'query': ['This field required']})

        results = search.basesearch(params['query'], user=request.user)
        serializer = SearchSerializer(results)

        return QuaApiResponse(serializer.data)
