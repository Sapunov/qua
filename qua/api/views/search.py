import logging

from rest_framework import views
from rest_framework.response import Response
from rest_framework import exceptions

from qua.api.search import search
from qua.api.serializers import SearchSerializer


log = logging.getLogger('qua.' + __name__)


class SearchView(views.APIView):
    def get(self, request, format=None):
        params = request.query_params

        if 'query' not in params:
            raise exceptions.ValidationError({'query': ['This field required']})

        if 'category' in params:
            try:
                category = int(params['category'])
            except ValueError:
                raise exceptions.ValidationError({'category': ['One integer required']})
        else:
            category = None

        results = search(
            params['query'], user=request.user, category=category)
        serializer = SearchSerializer(results)

        return Response(serializer.data)
