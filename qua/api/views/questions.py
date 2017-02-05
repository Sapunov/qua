import logging

from rest_framework.views import APIView
from django.conf import settings

from qua.api.serializers import QuestionSerializer, QuestionListSerializer
from qua.api.serializers import serialize, deserialize
from qua.api.response import QuaApiResponse
from qua.api.models import Question
from qua.api.tracker import trackable
from qua.api.pagination import paginate


log = logging.getLogger('qua.' + __name__)


class QuestionListView(APIView):

    @paginate
    def get(self, request, format=None, limit=settings.PAGE_SIZE, offset=0):

        questions = Question.get(limit=limit, offset=offset)
        serializer = serialize(QuestionListSerializer, questions)

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
        question.archive(user=request.user)

        return QuaApiResponse()
