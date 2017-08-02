from django.conf import settings
from rest_framework import serializers


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


class SearchRequest(serializers.Serializer):

    query = serializers.CharField()
    limit = serializers.IntegerField(default=settings.DEFAULT_PAGE_SIZE)
    offset = serializers.IntegerField(default=0)
    spelling = serializers.BooleanField(default=True)


class SearchHit(serializers.Serializer):

    _item_id = serializers.CharField()
    _type = serializers.CharField()
    _score = serializers.FloatField()
    _loc = serializers.CharField()
    ext_id = serializers.IntegerField()
    title = serializers.CharField()
    keywords = serializers.ListField(child=serializers.CharField())
    is_external = serializers.BooleanField()
    resource = serializers.CharField(allow_null=True)
    snippet = serializers.CharField()
    image = serializers.CharField(allow_null=True)


class SearchResponse(serializers.Serializer):

    query = serializers.CharField()
    total = serializers.IntegerField()
    hits = SearchHit(many=True)
    suggested_query = serializers.CharField()
    max_score = serializers.FloatField()
    min_score = serializers.FloatField()


class IndexRequest(serializers.Serializer):

    ext_id = serializers.IntegerField()
    title = serializers.CharField()
    text = serializers.CharField()
    keywords = serializers.ListField(child=serializers.CharField(), default=[])
    is_external = serializers.BooleanField(default=False)
    resource = serializers.CharField(default=None, allow_null=True)


class ItemUpdate(serializers.Serializer):

    keywords = serializers.ListField(
        child=serializers.CharField(), required=False)
    resource = serializers.CharField(required=False)
    text = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
