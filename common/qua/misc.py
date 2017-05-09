from datetime import datetime
from hashlib import sha1
from importlib import import_module
from urllib.parse import urlparse
import os
import tempfile


def sha1_hash(string):

    return sha1(string.encode('utf-8')).hexdigest()


def was_file_modified(path, from_time, raise_exception=True):
    '''Whether the file was modified since from_time

    :params:
        - path - path to file
        - from_time - datetime obj
        - raise_exeption - raise of not?
    '''

    if not os.path.isfile(path):
        if raise_exception:
            raise ValueError('File does not exists or directory')
        else:
            return False

    if not isinstance(from_time, datetime):
        raise ValueError('`from_time` must be datetime object')

    modif_time = os.path.getmtime(path)

    return datetime.fromtimestamp(modif_time) > from_time


def keyboard_layout_inverse(string):

    dic = {
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u',
        'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's',
        'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l',
        'ж': ';', 'э': '\'', 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b',
        'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.', 'ё': '`', 'q': 'й', 'w': 'ц',
        'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ',
        'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а',
        'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', '\'': 'э',
        'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь',
        ',': 'б', '.': 'ю', '`': 'ё'
    }

    result = ''

    for letter in string:
        result += dic.get(letter, letter)

    return result


def remove_empty_values(data):

    if isinstance(data, dict):
        clear_dict = {}

        for key, value in data.items():
            cleared_value = remove_empty_values(value)
            if cleared_value:
                clear_dict[key] = cleared_value

        return clear_dict
    elif isinstance(data, list):
        clear_list = []

        for item in data:
            cleared_value = remove_empty_values(item)
            if cleared_value:
                clear_list.append(cleared_value)

        return clear_list
    else:
        return data if data else False


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


def is_sign_ok(input_sign, string, secret_key, length=20):

    return input_sign == sign(string, secret_key, length=length)


def int2hex_id(integer):

    return hex(integer)[2:].zfill(8)


def hex_id2int(hex_id):

    return int(hex_id, 16)
