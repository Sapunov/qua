from django.conf import settings
from rest_framework import serializers


def deserialize(serializer_class, data, **kwargs):
    """Deserialize python dict to rest_framework class"""

    serializer = serializer_class(data=data, **kwargs)
    serializer.is_valid(raise_exception=True)

    return serializer


def serialize(serializer_class, instance, data=None, **kwargs):
    """Serialize rest_framework class to python dict"""

    if data is None:
        serializer = serializer_class(instance, **kwargs)
    else:
        serializer = serializer_class(instance, data=data, **kwargs)
        serializer.is_valid(raise_exception=True)

    return serializer


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
    prefix = serializers.CharField()
