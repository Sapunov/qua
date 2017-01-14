from rest_framework.exceptions import NotFound


def get_object(cls, pk):
    try:
        return cls.objects.get(pk=pk)
    except cls.DoesNotExist:
        raise NotFound
