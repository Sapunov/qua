from rest_framework.views import APIView

from qua.rest.response import QuaApiResponse
from qua.rest.serializers import serialize, deserialize
from qua.search import index as search_index
from search import serializers


class Search(APIView):

    def get(self, request):

        req_serializer = deserialize(
            serializers.SearchRequest,
            request.query_params)

        return QuaApiResponse(req_serializer.data)


class Index(APIView):

    def post(self, request):

        req_serializer = deserialize(serializers.IndexRequest, request.data)

        item_id = search_index.index_item(
            ext_id=req_serializer.data['ext_id'],
            title=req_serializer.data['title'],
            text=req_serializer.data['text'],
            keywords=req_serializer.data['keywords'],
            is_external=req_serializer.data['is_external'],
            resource=req_serializer.data['resource'])

        return QuaApiResponse({'item_id': item_id})

    def delete(self, request):

        search_index.clear_index()

        return QuaApiResponse()


class Items(APIView):

    def get(self, request, item_id):

        pass

    def put(self, request, item_id):

        pass

    def delete(self, request, item_id):

        search_index.delete_item(item_id)

        return QuaApiResponse()
