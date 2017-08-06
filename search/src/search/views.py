from rest_framework.response import Response
from rest_framework.views import APIView

from search.engine import index as engine_index
from search.engine import search

from search import serializers
from search.serializers import serialize, deserialize


class Search(APIView):

    def get(self, request):

        req_serializer = deserialize(
            serializers.SearchRequest,
            request.query_params)

        search_results = search.search_items(
            query=req_serializer.data['query'],
            limit=req_serializer.data['limit'],
            offset=req_serializer.data['offset'],
            spelling=req_serializer.data['spelling'])

        resp_serializer = serialize(serializers.SearchResponse, search_results)

        return Response(resp_serializer.data)


class Index(APIView):

    def post(self, request):

        req_serializer = deserialize(serializers.IndexRequest, request.data)

        item_id = engine_index.index_item(
            ext_id=req_serializer.data['ext_id'],
            title=req_serializer.data['title'],
            text=req_serializer.data['text'],
            keywords=req_serializer.data['keywords'],
            is_external=req_serializer.data['is_external'],
            resource=req_serializer.data['resource'])

        return Response({'item_id': item_id})

    def delete(self, request):

        engine_index.clear_index()

        return Response({})


class Items(APIView):

    def get(self, request, item_id):

        item = engine_index.get_item(item_id)

        return Response(item)

    def put(self, request, item_id):

        req_serializer = deserialize(serializers.ItemUpdate, request.data)

        item = engine_index.update_item(item_id, req_serializer.data)

        return Response(item)

    def delete(self, request, item_id):

        engine_index.delete_item(item_id)

        return Response({})
