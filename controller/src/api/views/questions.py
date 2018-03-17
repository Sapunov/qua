import logging

from django.conf import settings
from rest_framework.views import APIView

from api.models import Question
from api.pagination import paginate
from api.serializers import QuestionSerializer, QuestionListSerializer
from api.serializers import serialize, deserialize
from api.tracker import trackable
from app.response import QuaApiResponse


log = logging.getLogger(settings.APP_NAME + __name__)


class QuestionListView(APIView):

    @paginate
    def get(self, request, limit=settings.PAGE_SIZE, offset=0):
        '''Get list of questions'''

        questions = Question.get(limit=limit, offset=offset)
        serializer = serialize(QuestionListSerializer, questions)

        return QuaApiResponse(serializer.data)

    def post(self, request):
        '''Create new question'''

        serializer = deserialize(QuestionSerializer, data=request.data)
        serializer.save(user=request.user)

        return QuaApiResponse(serializer.data)


class QuestionView(APIView):

    @trackable
    def get(self, request, question_id):
        '''Get question by question_id'''

        question = Question.get(pk=question_id)
        serializer = serialize(QuestionSerializer, question)

        return QuaApiResponse(serializer.data)

    def put(self, request, question_id):
        '''Update question information'''

        question = Question.get(pk=question_id)
        serializer = serialize(QuestionSerializer, question, data=request.data)

        serializer.save(user=request.user)

        return QuaApiResponse(serializer.data)

    def delete(self, request, question_id):
        '''Delete the specific question'''

        question = Question.get(pk=question_id)
        question.archive(user=request.user)

        return QuaApiResponse()
