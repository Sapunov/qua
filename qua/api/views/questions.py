from rest_framework import views, status
from django.http import Http404

from qua.api.response import QuaApiResponse
from qua.api.models import Questions
from qua.api import serializers
from qua.api.tracker import trackable

import logging

log = logging.getLogger('qua.' + __name__)


class QuestionsBase(views.APIView):
    def get_object(self, pk):
        try:
            return Questions.objects.get(pk=pk, deleted=False)
        except Questions.DoesNotExist:
            raise Http404


class QuestionsListView(QuestionsBase):
    def get(self, request, format=None):
        questions = Questions.objects.all()
        params = request.query_params

        if 'category' in params:
            questions = questions.filter(categories=params['category'])

        serializer = serializers.QuestionsListSerializer(questions, many=True)

        return QuaApiResponse(serializer.data)

    def post(self, request, format=None):
        log.debug('Request data: %s', request.data)

        serializer = serializers.QuestionsDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return QuaApiResponse(serializer.data, status=status.HTTP_201_CREATED)


class QuestionsDetailView(QuestionsBase):
    @trackable
    def get(self, request, question_id, format=None):
        question = self.get_object(question_id)
        serializer = serializers.QuestionsDetailSerializer(question)

        return QuaApiResponse(serializer.data)

    def put(self, request, question_id, format=None):
        question = self.get_object(question_id)

        serializer = serializers.QuestionsDetailSerializer(
            question, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return QuaApiResponse(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, question_id, format=None):
        question = self.get_object(question_id)
        question.archive()

        return QuaApiResponse(status=status.HTTP_204_NO_CONTENT)
