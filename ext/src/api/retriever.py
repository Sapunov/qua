from urllib.parse import urljoin
import logging
import requests

from django.conf import settings

from api import misc
from api import models


log = logging.getLogger(settings.APP_NAME + __name__)


class BaseRetriever:
    '''Base retriever for all user defined retrievers'''

    # The hostname of the resource. Using in some methods.
    # MUST be provided in child methods
    base = None

    # Cannot use None because None returns when there is no settings for
    # the specific base
    _settings = misc.NotInitialized()

    def retrieve_page(self, url):
        '''Must be implemented in child classes. Calls when retrieving page'''

        try:
            req = requests.get(url, timeout=30)
        except requests.exceptions.RequestException as exc:
            log.exception('Exception while retrieving %s: %s', url, exc)
            return None

        if req.status_code != 200:
            log.error('Return code from %s is %s', url, req.status_code)
            return None

        return req.text

    @property
    def settings(self):
        '''Returns settings class with data from database'''

        assert self.base is not None, 'self.base must not be None'

        class ResourceSettings:
            '''Settings class created to limit fields for users'''

            def __init__(self, django_obj):

                self.hostname = django_obj.hostname
                self.scheme = django_obj.scheme
                self.login = django_obj.login
                self.password = django_obj.password

            def __str__(self):

                return '<ResourceSettings: {0}>'.format(self.hostname)

        if isinstance(self._settings, misc.NotInitialized):
            try:
                self._settings = ResourceSettings(
                    models.ExternalResourceSettings.objects.get(
                        hostname=self.base))
            except models.ExternalResourceSettings.DoesNotExist:
                self._settings = None

        return self._settings


def retrieve_url(url):
    '''Returns text from url in HTML format ALWAYS'''

    hostname = misc.extract_hostname(url)

    module_name = misc.removedots(hostname)
    class_name = misc.hostname2camelcase(hostname)

    try:
        class_ = misc.import_module_class(
            'api.extresources.{0}.{1}'.format(module_name, class_name))

        retriever = class_()
    except ImportError:
        retriever = BaseRetriever()

    return retriever.retrieve_page(url)
