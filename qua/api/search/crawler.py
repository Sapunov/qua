import os
import requests
import logging

import textract
from django.conf import settings

from qua.api.utils import common
from qua.api.search import utils as search_utils


log = logging.getLogger('qua.' + __name__)


def download_image(image_url):
    pass


def _get_content_type(content_type):

    CONTENT_TYPES = {
        'text/html': 'text',
        'application/pdf': 'pdf'
    }

    for c_type in CONTENT_TYPES:
        if c_type in content_type:
            return CONTENT_TYPES[c_type]

    return None


def _check_content_type(content_type, permitted):

    for c_type in permitted:
        if c_type in content_type:
            return _get_content_type(content_type)

    return False


class FormatConvertor:

    @classmethod
    def pdf(cls, data):

        temp_file = common.temp_file(data, suffix='.pdf', binary=True)

        try:
            text = textract.process(temp_file)
        except Exception as e:
            log.exception('TexttracException: %s', e)
            return None
        finally:
            os.remove(temp_file)

        try:
            decoded = text.decode('utf-8')
        except UnicodeDecodeError:
            log.exception('UnicodeDecodeError exception while decoding %s', temp_file)
            return None

        text = search_utils.deduplicate_spaces(decoded)

        title, body = cls.extract_title_body(text)

        return cls.as_html(title, body)

    @classmethod
    def extract_title_body(cls, text):

        try:
            first_dot = text.index('.')
        except ValueError:
            first_dot = 100

        title = text[:first_dot]
        body = text[first_dot + 1:]

        return title, body

    @classmethod
    def can_format(cls, format_name):

        return hasattr(cls, format_name)

    @classmethod
    def format(cls, data, format_name):

        # TODO: check if attr `format_name exists`
        return getattr(cls, format_name)(data)

    @classmethod
    def as_html(cls, title, body):

        return '<title>{0}<title><body>{1}</body>'.format(title, body)


def retrieve_page(url):

    log.debug('Trying to retieve page: %s', url)

    try:
        r = requests.get(url, timeout=30)
    except requests.exceptions.RequestException as e:
        log.exception('Exception while retrieving %s: %s', url, e)

        return None

    if r.status_code != 200:
        return None

    content_type = _check_content_type(
        r.headers.get('Content-Type', ''),
        settings.CRAWLER['permitted_content_types']
    )

    log.debug('Content-Type of the %s - %s', url, content_type)

    if content_type is None:
        return None

    if content_type != 'text':
        if FormatConvertor.can_format(content_type):
            return FormatConvertor.format(r.content, content_type)
    else:
        return r.text
