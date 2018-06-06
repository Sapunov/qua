import string
import random
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.six import text_type
from rest_framework import HTTP_HEADER_ENCODING


def is_email(text):

    try:
        validate_email(text)
        return True
    except ValidationError:
        return False


def get_random_string(length, dictionary=None):

    if dictionary is None:
        dictionary = string.ascii_letters + string.digits

    return ''.join(random.choice(dictionary) for _ in range(length))


def add_param_to_url(url, param_name, param_value, raise_duplicate=True):

    url_parts = list(urlparse(url))
    query_params = parse_qs(url_parts[4])

    param_name = param_name.lower()

    if param_name in query_params and raise_duplicate:
        raise ValueError('Duplicate param: %s' % param_name)

    if param_name not in query_params:
        query_params[param_name] = []

    query_params[param_name].append(param_value)

    url_parts[4] = urlencode(query_params, doseq=True)

    return urlunparse(url_parts)


def get_header(request, header_name):

    header = request.META.get(header_name, b'')

    if isinstance(header, text_type):
        header = header.encode(HTTP_HEADER_ENCODING)

    try:
        header = header.decode()
    except UnicodeError:
        header = None

    return header
