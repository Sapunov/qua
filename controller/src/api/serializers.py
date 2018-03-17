import logging

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import django_rq

from api import tasks
from api.models import Question, Keyword, Answer, ExternalResource


log = logging.getLogger(settings.APP_NAME + __name__)
queue = django_rq.get_queue(settings.APP_NAME)


def deserialize(serializer_class, data, **kwargs):
    '''Deserialize python dict to rest_framework class'''

    serializer = serializer_class(data=data, **kwargs)
    serializer.is_valid(raise_exception=True)

    return serializer


def serialize(serializer_class, instance, data=None, **kwargs):
    '''Serialize rest_framework class to python dict'''

    if data is None:
        serializer = serializer_class(instance, **kwargs)
    else:
        serializer = serializer_class(instance, data=data, **kwargs)
        serializer.is_valid(raise_exception=True)

    return serializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)


class AutoUpdatePrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def __init__(self, model, **kwargs):

        self.model = model
        super(AutoUpdatePrimaryKeyRelatedField, self).__init__(**kwargs)

    def get_queryset(self, data):

        try:
            return self.model.get_or_create(data)
        except AttributeError:
            raise AttributeError('Model must have "get_or_create" method')

    def to_internal_value(self, data):

        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)

        try:
            return self.get_queryset(data)[0]
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)


class UserSerializer(DynamicFieldsModelSerializer):

    class Meta:

        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AnswerSerializer(DynamicFieldsModelSerializer):

    raw = serializers.CharField(allow_blank=True)
    html = serializers.CharField(required=False)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        exclude = ('id', 'question')


class QuestionSerializer(DynamicFieldsModelSerializer):
    '''Serialize question'''

    title = serializers.CharField(max_length=300, required=False)
    keywords = AutoUpdatePrimaryKeyRelatedField(
        model=Keyword,
        many=True,
        required=False)
    answer = AnswerSerializer(required=False)
    answer_exists = serializers.BooleanField(required=False)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    def create(self, validated_data):
        '''Create new question from validated_data'''

        if 'title' not in validated_data:
            raise ValidationError({'title': ['This field is required.']})

        question = Question.create(
            validated_data['title'],
            validated_data['user'],
            keywords=validated_data.get('keywords', None)
        )

        if 'answer' in validated_data and validated_data['answer'] != '':
            Answer.create(
                validated_data['answer']['raw'],
                validated_data['user'],
                question
            )

        # Send question to the search microservice via message queue
        queue.enqueue(tasks.index_question, question)

        return question

    def update(self, instance, validated_data):
        '''Update existing question by validated_data'''

        instance.update(
            validated_data['user'],
            title=validated_data.get('title', None),
            keywords=validated_data.get('keywords', None)
        )

        if 'answer' in validated_data:
            if instance.answer_exists:
                if validated_data['answer']['raw'] == '':
                    instance.answer.delete()
                    instance.answer = None
                else:
                    log.debug('Trying to update %s', instance.answer.name)

                    instance.answer.update(
                        validated_data['answer']['raw'],
                        validated_data['user']
                    )
            else:
                log.debug('Creating new answer for %s', instance)

                Answer.create(
                    validated_data['answer']['raw'],
                    validated_data['user'],
                    instance
                )

        instance.save()

        # Send question to the search microservice via message queue
        queue.enqueue(tasks.reindex_question, instance)

        return instance

    class Meta:

        model = Question
        exclude = ('deleted', 'se_id')


class QuestionListSerializer(serializers.Serializer):

    total = serializers.IntegerField()
    items = QuestionSerializer(many=True, fields=(
        'answer_exists', 'title', 'keywords', 'created_at', 'created_by',
        'updated_at', 'updated_by', 'id'))


class UrlParamsSerializer(serializers.Serializer):

    shid = serializers.IntegerField()
    qid = serializers.IntegerField()
    token = serializers.CharField()
    track = serializers.CharField()


class SearchHitSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField()
    snippet = serializers.CharField()
    score = serializers.FloatField()
    keywords = serializers.ListField(child=serializers.CharField())
    image = serializers.CharField()
    url_params = UrlParamsSerializer(required=False)
    url = serializers.URLField(required=False)
    is_external = serializers.BooleanField()
    resource = serializers.URLField(allow_null=True)


class SearchSerializer(serializers.Serializer):

    query = serializers.CharField()
    total = serializers.IntegerField()
    hits = SearchHitSerializer(many=True)
    query_was_corrected = serializers.BooleanField()
    used_query = serializers.CharField()
    took = serializers.FloatField()


class SearchRequest(serializers.Serializer):

    query = serializers.CharField()
    limit = serializers.IntegerField(default=settings.PAGE_SIZE)
    offset = serializers.IntegerField(default=0)


class ExtResource(DynamicFieldsModelSerializer):
    '''External resource serializer'''

    title = serializers.CharField(required=False)
    scheme = serializers.CharField(required=False)
    hostname = serializers.CharField(required=False)
    url = serializers.URLField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    def create(self, validated_data):
        '''Create new external resource by valudated_data'''
        ext_resource, created = ExternalResource.create(
            validated_data['url'], validated_data['user'])

        if created:
            if not ext_resource.index_resource():
                ext_resource.delete()
                raise ValidationError({
                    'error_msg': 'Cannot index {0}'.format(
                        validated_data['url'])})
        else:
            raise ValidationError({
                'error_msg': 'Resource {0} already exists'.format(
                    validated_data['url'])})

        return ext_resource

    class Meta:

        model = ExternalResource
        exclude = ('se_id', 'update_interval', '_content_hash', '_url')


class ExtResourceList(serializers.Serializer):

    total = serializers.IntegerField()
    items = ExtResource(many=True)
