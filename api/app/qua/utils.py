from hashlib import sha256
from importlib import import_module
from urllib.parse import urlparse
import logging

from django.conf import settings


log = logging.getLogger('qua.' + __name__)


def sign(string, length=20):

    string += settings.SECRET_KEY
    string = bytes(string, 'utf-8')
    sha256_hash = sha256(string)

    return sha256_hash.hexdigest()[0:length]


def is_sign_ok(input_sign, string, length=20):

    return input_sign == sign(string, length=length)


def url_part(url, part_name):

    parsed = urlparse(url)

    if hasattr(parsed, part_name):
        return getattr(parsed, part_name)


def extract_domain(url):

    netloc = url_part(url, 'netloc')

    return netloc if netloc else None


def import_module_class(name):

    module_name, class_name = name.rsplit('.', 1)

    module = import_module(module_name)

    try:
        class_ = getattr(module, class_name)
    except AttributeError:
        raise ImportError('No class <%s> in %s' % (class_name, module))

    return class_
