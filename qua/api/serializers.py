import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from qua.api.models import Category, Question, Keyword, Answer
from qua.api import tasks


log = logging.getLogger('qua.' + __name__)


def deserialize(serializer_class, data):

    log.debug('Deserializing %s with %s', data, serializer_class)

    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)

    log.debug('Validated data: %s', serializer.validated_data)

    return serializer

def serialize(serializer_class, instance, data=None, **kwargs):

    log.debug('Serializing %s with %s for %s. Kwargs: %s',
        data, serializer_class, instance, kwargs)

    if data is None:
        serializer = serializer_class(instance, **kwargs)
    else:
        serializer = serializer_class(instance, data=data, **kwargs)
        serializer.is_valid(raise_exception=True)

        log.debug('Validated data: %s', serializer.validated_data)

    return serializer


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


class PrimaryKeyExistsValidator:
    def __init__(self, queryset, message=None):
        self.queryset = queryset
        self.message = message or 'Item with primary key {primary_key} does not exist'

    def __call__(self, value):
        assert ('id' in value and isinstance(value, dict)), 'Value must be a "dict" with "id" element'

        try:
            self.queryset.get(pk=value['id'])
        except ObjectDoesNotExist:
            raise ValidationError(self.message.format(primary_key=value['id']))


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class CategoryListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(DynamicFieldsModelSerializer):

    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=50, required=False)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    def create(self, validated_data):
        if 'name' not in validated_data:
            raise ValidationError({'name': ['This field is required.']})

        return Category.create(validated_data['name'], validated_data['user'])

    def update(self, instance, validated_data):
        if 'name' not in validated_data:
            raise ValidationError({'name': ['This field is required.']})

        instance.name = validated_data['name']
        instance.updated_by = validated_data['user']

        instance.save()

        return instance

    class Meta:
        model = Category
        fields = '__all__'


class AnswerSerializer(DynamicFieldsModelSerializer):
    html = serializers.CharField(required=False)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        exclude = ('id', 'question')


class QuestionListSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True, fields=('id', 'name'))
    keywords = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='text')

    answer_exists = serializers.BooleanField()

    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Question
        exclude = ('deleted',)


class QuestionSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=300, required=False)
    categories = CategorySerializer(
        many=True,
        fields=('id', 'name'),
        validators=[PrimaryKeyExistsValidator(
            queryset=Category.objects.all(),
            message='Category with primary key {primary_key} does not exist'
        )],
        required=False
    )
    keywords = AutoUpdatePrimaryKeyRelatedField(model=Keyword, many=True, required=False)
    answer = AnswerSerializer(required=False)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    def create(self, validated_data):
        if 'title' not in validated_data:
            raise ValidationError({'title': ['This field is required.']})

        if 'categories' in validated_data:
            category_ids = [cat['id'] for cat in validated_data['categories']]
        else:
            category_ids = None

        question = Question.create(
            validated_data['title'],
            validated_data['user'],
            keywords=validated_data.get('keywords', None),
            category_ids=category_ids
        )

        if 'answer' in validated_data:
            Answer.create(
                validated_data['answer']['raw'],
                validated_data['user'],
                question
            )

        tasks.index_question.delay(question.id)

        return question

    def update(self, instance, validated_data):
        if 'categories' in validated_data:
            category_ids = [cat['id'] for cat in validated_data['categories']]
        else:
            category_ids = None

        instance.update(
            validated_data['user'],
            title=validated_data.get('title', None),
            keywords=validated_data.get('keywords', None),
            category_ids=category_ids
        )

        if 'answer' in validated_data:
            if instance.answer_exists:
                instance.answer.update(
                    validated_data['answer']['raw'],
                    validated_data['user']
                )
            else:
                Answer.create(
                    validated_data['answer']['raw'],
                    validated_data['user'],
                    instance
                )

        tasks.index_question.delay(instance.id)

        return instance

    class Meta:
        model = Question
        exclude = ('deleted',)


class CategoryAssumptionsSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    score = serializers.FloatField()


class UrlParamsSerializer(serializers.Serializer):

    shid = serializers.IntegerField()
    qid = serializers.IntegerField()
    token = serializers.CharField()
    track = serializers.CharField()


class SearchHitSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField()
    categories = CategorySerializer(many=True, fields=('id', 'name'))
    snippet = serializers.CharField()
    score = serializers.FloatField()
    keywords = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='text')
    image = serializers.CharField()
    url_params = UrlParamsSerializer()


class SearchSerializer(serializers.Serializer):

    query = serializers.CharField()
    total = serializers.IntegerField()
    hits = SearchHitSerializer(many=True)
    category_assumptions = CategoryAssumptionsSerializer(many=True)
