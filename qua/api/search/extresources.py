import re
import json
import requests
import logging
from urllib.parse import urljoin

from qua import utils


log = logging.getLogger('qua.' + '__name__')


class BaseRetriever:

    base = ''

    auth_type = None
    username = None
    password = None

    def __init__(self, configuration):

        if 'auth' in configuration:
            self.auth_type = configuration['auth'].get('type', None)

            self.username = configuration['auth']['username']
            self.password = configuration['auth']['password']

    def retrieve_page(self, url):

        raise NotImplementedError('`retrieve_page` must be implemented')

    def join_url(self, path):

        return urljoin(self.base, path)

    def try_json(self, text):

        try:
            first_bracket = text.index('{')
        except ValueError:
            return text

        try:
            return json.loads(text[first_bracket:])
        except ValueError:
            return text

    def as_html(self, title, body):

        return '<title>{0}<title><body>{1}</body>'.format(title, body)


class JiveCrocRu(BaseRetriever):

    base = 'https://jive.croc.ru'

    document_regexp = r'/docs/DOC-(\d+)'
    document_type_id = 102

    def retrieve_page(self, url):

        path = utils.url_part(url, 'path')

        if re.match(self.document_regexp, path) is not None:
            return self._retrieve_document(url)
        else:
            return self._authorized_request(url)

    def _get_docid(self, url):

        path = utils.url_part(url, 'path')

        finded = re.findall(self.document_regexp, path)

        if finded:
            return int(finded[0])

    def _retrieve_document(self, url):

        docid = self._get_docid(url)
        api_url = self.join_url(
            'api/core/v3/contents?filter=entityDescriptor({0}, {1})'.format(
                self.document_type_id,
                docid
            )
        )

        response = self._authorized_request(api_url)

        try:
            title = response['list'][0]['subject']
            body = response['list'][0]['content']['text']
        except (KeyError, IndexError):
            return False

        return self.as_html(title, body)

    def _authorized_request(self, url):

        if self.auth_type != 'basic':
            return None

        try:
            r = requests.get(url, timeout=30, auth=(self.username, self.password))
        except requests.exceptions.RequestException as e:
            log.exception('Exception while retrieving %s: %s', url, e)

            return None

        if r.status_code != 200:
            return None

        return self.try_json(r.text)

    def as_html(self, title, body):

        return '<title>{0}<title>{1}'.format(title, body)
