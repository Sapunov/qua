from datetime import datetime
from hashlib import sha1
import os


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
