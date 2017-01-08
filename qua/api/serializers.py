import logging

from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction

from qua.api import models
from qua.api.utils import common


log = logging.getLogger('qua.' + __name__)


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
        fields = ('id', 'username', 'first_name', 'last_name', 'is_active', 'email')


class CategoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categories
        fields = '__all__'

    created_by = UserSerializer(
        read_only=True, fields=('id', 'username', 'first_name', 'last_name'))
    updated_by = UserSerializer(
        read_only=True, fields=('id', 'username', 'first_name', 'last_name'))


class CategoriesDetailSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.Categories
        fields = '__all__'

    created_by = UserSerializer(
        read_only=True, fields=('id', 'username', 'first_name', 'last_name'))
    updated_by = UserSerializer(
        read_only=True, fields=('id', 'username', 'first_name', 'last_name'))

    def create(self, validated_data):
        validated_data['created_by'] = validated_data.pop('user')
        validated_data['updated_by'] = validated_data['created_by']

        return models.Categories.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'name' not in validated_data:
            return instance

        instance.name = validated_data['name']
        instance.updated_by = validated_data['user']

        instance.save()

        return instance


class AnswerSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.Answers
        fields = ('id', 'html', 'version', 'created_at', 'created_by',
            'updated_at', 'updated_by', 'snippet', 'raw')

    created_by = UserSerializer(
        fields=('id', 'username', 'first_name', 'last_name'))
    updated_by = UserSerializer(
        fields=('id', 'username', 'first_name', 'last_name'))


class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Keywords
        fields = '__all__'


class QuestionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Questions
        fields = ('id', 'title', 'categories', 'answer', 'keywords',
            'created_at', 'created_by', 'updated_at', 'updated_by')

    categories = CategoriesDetailSerializer(many=True, fields=('id', 'name'))
    answer = AnswerSerializer(read_only=True, fields=(
        'snippet', 'created_by', 'created_at', 'updated_by', 'updated_at'))
    keywords = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='text')
    created_by = UserSerializer(
        read_only=True, fields=('id', 'username', 'first_name', 'last_name'))
    updated_by = UserSerializer(
        read_only=True, fields=('id', 'username', 'first_name', 'last_name'))


class QuestionsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Questions
        fields = ('id', 'title', 'categories', 'answer', 'keywords',
            'created_at', 'created_by', 'updated_at', 'updated_by')

    title = serializers.CharField(max_length=200, required=False)
    categories = CategoriesDetailSerializer(
        many=True, read_only=True, fields=('id', 'name'))
    answer = AnswerSerializer(read_only=True)
    keywords = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='text')
    created_by = UserSerializer(
        read_only=True, fields=('id', 'username', 'first_name', 'last_name'))
    updated_by = UserSerializer(
        read_only=True, fields=('id', 'username', 'first_name', 'last_name'))

    @transaction.atomic
    def create(self, validated_data):
        log.debug('Initial data: %s', self.initial_data)

        user = validated_data['user']
        data = self.initial_data

        if 'title' not in data:
            raise serializers.ValidationError({'title': ['This field is required']})

        question = models.Questions.objects.create(
            title=validated_data['title'], created_by=user, updated_by=user)

        if 'keywords' in data:
            keywords = models.Keywords.ensure_exists(data['keywords'])
            question.keywords = keywords

        if 'categories' in data:
            log.debug('Categories: %s', data['categories'])
            try:
                category_ids = common.ensure_list(
                    data['categories'], to_int=True)
            except ValueError:
                raise serializers.ValidationError({'categories': ['List of integers required']})

            if models.Categories.objects.filter(
                pk__in=category_ids).count() != len(category_ids):
                raise serializers.ValidationError(
                    {'categories': ['Specified categories doesn\'t exists']})

            question.categories = models.Categories.objects.filter(
                pk__in=category_ids)

        question.save()

        if 'answer' in data:
            if 'raw' not in data['answer']:
                raise serializers.ValidationError({'answer.raw': ['This field is required']})

            models.Answers.create(raw=data['answer']['raw'],
                user=user, question=question,
                snippet=data['answer'].get('snippet', None))

        return question

    def update(self, instance, validated_data):
        log.debug('Validated_data: %s, Instance: %s, Initial_data: %s',
            validated_data, instance, self.initial_data)

        user = validated_data['user']
        data = self.initial_data

        if 'title' in data:
            instance.title = data['title']

        if 'categories' in data:
            log.debug('Categories: %s', data['categories'])
            try:
                category_ids = common.ensure_list(
                    data['categories'], to_int=True)
            except ValueError:
                raise serializers.ValidationError({'categories': ['List of integers required']})

            if models.Categories.objects.filter(
                pk__in=category_ids).count() != len(category_ids):
                raise serializers.ValidationError(
                    {'categories': ['Specified categories doesn\'t exist']})

            question.categories = models.Categories.objects.filter(
                pk__in=category_ids)

        if 'keywords' in data:
            instance.keywords = models.Keywords.ensure_exists(data['keywords'])

        if 'answer' in data:
            try:
                answer = models.Answers.objects.get(question__pk=instance.id)

                if 'raw' in data['answer']:
                    answer.raw = data['answer']['raw']
                    answer.version += 1

                if 'snippet' in data['answer']:
                    answer.snippet = data['answer']['snippet']

                answer.save()
            except models.Answers.DoesNotExist:
                if 'raw' not in data['answer']:
                    raise serializers.ValidationError({'answer.raw': ['This field is required']})

                answer = models.Answers.create(
                    raw=data['answer']['raw'], user=user, question=instance,
                    snippet=data['answer'].get('snippet', None))

            instance.answer = answer

        instance.updated_by = user

        instance.save()

        return instance


class CategoryAssumptionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    score = serializers.FloatField()


class UrlParamsSerializer(serializers.Serializer):
    shid = serializers.IntegerField()
    qid = serializers.IntegerField()
    token = serializers.CharField()


class SearchHitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    categories = CategoriesDetailSerializer(many=True, fields=('id', 'name'))
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
