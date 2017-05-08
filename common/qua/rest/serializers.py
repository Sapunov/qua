from django.core.exceptions import ObjectDoesNotExist
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
