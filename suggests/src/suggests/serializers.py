from django.conf import settings

from rest_framework import serializers


class AccumulateRequest(serializers.Serializer):

    text = serializers.CharField()
    last = serializers.IntegerField(required=False)
    quick_ans = serializers.CharField(required=False)
    freq = serializers.IntegerField(required=False)


class SuggestRequest(serializers.Serializer):

    query = serializers.CharField(allow_blank=True)
    limit = serializers.IntegerField(
        required=False,
        default=settings.SUGGESTS_DEFAULT_LIMIT)


class SuggestAnswer(serializers.Serializer):

    text = serializers.CharField()
    rate = serializers.IntegerField()
    quick_ans = serializers.CharField()
