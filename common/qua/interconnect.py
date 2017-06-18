import random
import requests

from django.conf import settings

from qua import misc
from qua import settings as qua_settings
from qua import exceptions


assert hasattr(settings, 'SERVICES'), 'You must specify SERVICES'


def _request(method, name, **kwargs):

    # Each service may contains many instances
    hosts = misc.resolve_dots(name, settings.SERVICES)
    random.shuffle(hosts)

    kwargs['timeout'] = kwargs.get('timeout', qua_settings.SERVICES_TIMEOUT)

    for host in hosts:
        try:
            return requests.api.request(method, host, **kwargs)
        except requests.exceptions.RequestException as e:
            continue

    raise exceptions.InterconnectionError('No service can respond')


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
