import random
import requests
from json import JSONDecodeError

from django.conf import settings

# All services in current state is django-based, because of that
# variable `settings` is service specific, that's why if microservice
# wants to use this module it MUST specify SERVICES in their settings module
# otherwise exception will raise
#
# A good idea to make a separate service that responsible for service discovery

from api import exceptions
from api import misc

assert hasattr(settings, 'SERVICES'), 'You must specify SERVICES'


class InterconnectionResponse():

    def __init__(self, requests_response):

        self.status_code = requests_response.status_code
        self.data = requests_response.json()


def _request(method, name, **kwargs):

    host = misc.resolve_dots(name, settings.SERVICES)

    kwargs['timeout'] = kwargs.get('timeout', settings.SERVICES_TIMEOUT)

    try:
        req = requests.api.request(method, host, **kwargs)
    except requests.exceptions.RequestException as exc:
        raise exceptions.InterconnectionError(
            'Service `{0}` on `{1}` cannot respond'.format(name, host))

    return InterconnectionResponse(req)


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
