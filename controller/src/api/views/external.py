import logging

from django.conf import settings
from rest_framework.views import APIView
import django_rq

from api import serializers
from api import tasks
from api.models import ExternalResource
from api.pagination import paginate
from api.serializers import serialize, deserialize
from app.response import QuaApiResponse
from api import constants


log = logging.getLogger(settings.APP_NAME + __name__)
queue = django_rq.get_queue(settings.APP_NAME)


class ExtResources(APIView):

    @paginate
    def get(self, request, limit=settings.PAGE_SIZE, offset=0):
        '''Get list of external resources'''

        extresources = ExternalResource.get(limit=limit, offset=offset)
        serializer = serialize(serializers.ExtResourceList, extresources)

        return QuaApiResponse(serializer.data)

    def post(self, request):
        '''Create new external resource'''

        serializer = deserialize(serializers.ExtResource, data=request.data)
        serializer.save(user=request.user)

        return QuaApiResponse(serializer.data)


class ExtResource(APIView):

    def get(self, request, external_id):
        '''Get extresource by extresource_id'''

        extresource = ExternalResource.get(pk=external_id)
        serializer = serialize(serializers.ExtResource, extresource)

        return QuaApiResponse(serializer.data)

    def delete(self, request, external_id):
        '''Delete specific external resource'''

        try:
            extresource = ExternalResource.get(pk=external_id)
            extresource.delete()
        except Exception as exc:
            log.exception(exc)

        return QuaApiResponse()


class ExtResourceBulk(APIView):

    def post(self, request):
        '''Creates many external resources at a time'''

        serializer = deserialize(
            serializers.ExtResource, data=request.data, many=True)

        ans = []
        resources_list = []

        for resource in serializer.validated_data:
            tmp = {'url': resource['url'], 'status': 'queued'}

            if ExternalResource.is_exists(resource['url']):
                tmp['status'] = 'exists'
            else:
                resources_list.append(resource['url'])

            ans.append(tmp)

        queue.enqueue(
            tasks.index_external_resources,
            resources_list,
            request.user,
            timeout=constants.HOUR)

        return QuaApiResponse(ans)
