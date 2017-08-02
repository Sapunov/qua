from datetime import datetime
from hashlib import sha1
from importlib import import_module
from urllib.parse import urlparse
import os
import tempfile
import time


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


def word_normalize(phrase):

    words = [word.strip().lower() for word in phrase.split(' ')]

    return ' '.join([word for word in words if word])


def temp_file(data, suffix='', prefix='', binary=False):

    filepath = tempfile.mktemp(suffix=suffix, prefix=prefix)

    mode = 'wb' if binary else 'w'

    with open(filepath, mode) as fd:
        fd.write(data)

    return filepath


def h6(string):

    return sha1_hash(string)[:6]


def sign(string, secret_key, length=20):

    return sha1_hash(string + secret_key)[0:length]


def translit(string):

    dic = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'ju', 'я': 'ja', 'a': 'а',
        'b': 'б', 'c': 'ц', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'х',
        'i': 'и', 'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
        'p': 'п', 'q': 'q', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'v': 'в',
        'w': 'w', 'x': 'x', 'y': 'ы', 'z': 'з'
    }

    result = ''

    for letter in string:
        result += dic.get(letter, letter)

    return result
