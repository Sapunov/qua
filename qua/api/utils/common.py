def split_by(string, separator=','):
    return [item.strip() for item in string.split(separator)]


def word_normalize(word):
    word = word.strip().lower()
    return word.replace(' ', '_')


def ensure_list(list_or_str, separator=',', to_int=False):
    items = []

    if isinstance(list_or_str, str):
        items = split_by(list_or_str, separator)
    else:
        items = list(list_or_str)

    if to_int:
        items = [int(item) for item in items]

    return items


def snippet(text):
    return text[0:50]
