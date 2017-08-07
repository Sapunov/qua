import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from search import serializers
from search.engine import index as engine_index
from search.engine import search
from search.serializers import serialize, deserialize


log = logging.getLogger(settings.APP_NAME + '.' + __name__)


class Search(APIView):

    def get(self, request):

        req_serializer = deserialize(
            serializers.SearchRequest,
            request.query_params)

        log.debug('Serialized user query_params: %s', req_serializer.data)

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

        log.debug('Serialized user query_params: %s', req_serializer.data)

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

        log.debug('Serialized user query_params: %s', req_serializer.data)

        item = engine_index.update_item(item_id, req_serializer.data)

        return Response(item)

    def delete(self, request, item_id):

        engine_index.delete_item(item_id)

        return Response({})
