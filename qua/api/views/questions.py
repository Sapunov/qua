import logging

from rest_framework.views import APIView

from qua.api.serializers import QuestionSerializer, QuestionListSerializer
from qua.api.serializers import serialize, deserialize
from qua.api.response import QuaApiResponse
from qua.api.models import Question
from qua.api.tracker import trackable


log = logging.getLogger('qua.' + __name__)


class QuestionListView(APIView):
    def get(self, request, format=None):
        questions = Question.get(category=request.query_params.get('category', None))
        serializer = serialize(QuestionListSerializer, questions, many=True)

        return QuaApiResponse(serializer.data)

    def post(self, request, format=None):
        serializer = deserialize(QuestionSerializer, data=request.data)
        serializer.save(user=request.user)

        return QuaApiResponse(serializer.data)


class QuestionView(APIView):
    @trackable
    def get(self, request, question_id, format=None):
        question = Question.get(pk=question_id)
        serializer = serialize(QuestionSerializer, question)

        return QuaApiResponse(serializer.data)

    def put(self, request, question_id, format=None):
        question = Question.get(pk=question_id)
        serializer = serialize(QuestionSerializer, question, data=request.data)

        serializer.save(user=request.user)

        return QuaApiResponse(serializer.data)

    def delete(self, request, question_id, format=None):
        question = Question.get(pk=question_id)
        question.archive()

        return QuaApiResponse()
