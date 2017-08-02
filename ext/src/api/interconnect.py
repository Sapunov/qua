import random
import requests

# All services in current state is django-based, because of that
# variable `settings` is service specific, that's why if microservice
# wants to use this module it MUST specify SERVICES in their settings module
# otherwise exception will raise
#
# A good idea to make a separate service that responsible for service discovery
from django.conf import settings

from api import exceptions
from api import misc


assert hasattr(settings, 'SERVICES'), 'You must specify SERVICES'


def _request(method, name, **kwargs):

    host = misc.resolve_dots(name, settings.SERVICES)

    kwargs['timeout'] = kwargs.get('timeout', settings.SERVICES_TIMEOUT)

    try:
        return requests.api.request(method, host, **kwargs)
    except requests.exceptions.RequestException:
        raise exceptions.InterconnectionError(
            'Service `{0}` on `{1}` cannot respond'.format(name, host))


def get(name, **kwargs):

    return _request('get', name, **kwargs)


def post(name, **kwargs):

    return _request('post', name, **kwargs)


def put(name, **kwargs):

    return _request('put', name, **kwargs)


def delete(name, **kwargs):

    return _request('delete', name, **kwargs)


def head(name, **kwargs):

    return _request('head', name, **kwargs)


def patch(name, **kwargs):

    return _request('patch', name, **kwargs)


def options(name, **kwargs):

    return _request('options', name, **kwargs)
