from rest_framework import serializers

from qua import settings as qua_settings


class SearchRequest(serializers.Serializer):

    query = serializers.CharField()
    limit = serializers.IntegerField(default=qua_settings.SERP_SIZE)
    offset = serializers.IntegerField(default=0)


class SearchHit(serializers.Serializer):

    item_id = serializers.CharField()
    ext_id = serializers.IntegerField()
    title = serializers.CharField()
    keywords = serializers.ListField(child=serializers.CharField())
    is_external = serializers.BooleanField()
    resource = serializers.CharField(allow_null=True)
    score = serializers.FloatField()
    snippet = serializers.CharField()
    image = serializers.CharField(allow_null=True)


class SearchResponse(serializers.Serializer):

    query = serializers.CharField()
    total = serializers.IntegerField()
    hits = SearchHit(many=True)
    suggested_query = serializers.CharField()
    took = serializers.FloatField()


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
