from rest_framework.views import APIView

from app.response import QuaApiResponse
from suggests import models
from suggests import serializers
from suggests import tree
from suggests.serializers import serialize, deserialize


class Accumulate(APIView):

    def post(self, request):

        req_serializer = deserialize(
            serializers.AccumulateRequest,
            request.data,
            many=True)

        models.AccumulateQueue.add(req_serializer.data)

        return QuaApiResponse()


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

        return QuaApiResponse(resp_serializer.data)
