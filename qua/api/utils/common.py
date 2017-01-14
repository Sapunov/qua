import re
import hashlib


def word_normalize(phrase):
    words = re.findall(r'([\w_\-\@]+)', phrase, re.UNICODE)
    return ' '.join(word.lower() for word in words)


def snippet(text):
    return text[0:50]


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


def h6(string):
    byte_string = bytes(string, "utf-8")
    return hashlib.sha256(byte_string).hexdigest()[:6]
