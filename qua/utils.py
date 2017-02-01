import logging
from hashlib import sha256
from urllib.parse import urlparse

from django.conf import settings


log = logging.getLogger('qua.' + __name__)


def sign(string, length=20):

    string += settings.SECRET_KEY
    string = bytes(string, 'utf-8')
    sha256_hash = sha256(string)

    return sha256_hash.hexdigest()[0:length]


def is_sign_ok(input_sign, string, length=20):

    return input_sign == sign(string, length=length)


def extract_domain(url):

    o = urlparse(url)

    return o.netloc if o.netloc else None
