import logging

from django.conf import settings


def get_logger(name):

    return logging.getLogger(settings.APP_NAME + '.' + name)


def expand_context_for_logging(context):

    return {
        'view_name': context['view'].get_view_name(),
        'absolute_uri': context['request'].build_absolute_uri(),
        'http_method': context['request'].method,
        'user': context['request'].user
    }


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
