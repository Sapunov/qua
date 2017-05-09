from rest_framework import serializers

from qua import settings as qua_settings


class SearchRequest(serializers.Serializer):

    query = serializers.CharField()
    spelling = serializers.BooleanField(default=True)
    limit = serializers.IntegerField(default=qua_settings.SERP_SIZE)
    offset = serializers.IntegerField(default=0)


class IndexRequest(serializers.Serializer):

    ext_id = serializers.IntegerField()
    title = serializers.CharField()
    text = serializers.CharField()
    keywords = serializers.ListField(child=serializers.CharField(), default=[])
    is_external = serializers.BooleanField(default=False)
    resource = serializers.CharField(default=None)
