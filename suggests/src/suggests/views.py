from rest_framework.response import Response
from rest_framework.views import APIView

from qua.common import serialize, deserialize
from suggests import models
from suggests import serializers
from suggests import tree


class Accumulate(APIView):

    def post(self, request):

        req_serializer = deserialize(
            serializers.AccumulateRequest,
            request.data,
            many=True)

        models.AccumulateQueue.add(req_serializer.data)

        return Response()


class Suggest(APIView):

    def get(self, request):

        req_serializer = deserialize(
            serializers.SuggestRequest,
            request.query_params)

        resp_serializer = serialize(
            serializers.SuggestAnswer,
            tree.suggest(
                req_serializer.data['query'],
                req_serializer.data['limit']),
            many=True)

        return Response(resp_serializer.data)
