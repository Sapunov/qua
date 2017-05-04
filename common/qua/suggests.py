import re


def prepare_description(key, value, item, mapping, max_len=60):

    key_regexp = r'\{([a-z_]*?)\}'

    if key not in mapping:
        return [value]

    pattern = mapping[key]
    replace = {}

    for placeholder in re.findall(key_regexp, pattern):
        if placeholder not in item:
            pattern = pattern.replace('{%s}' % placeholder, '')
        else:
            replace[placeholder] = item[placeholder]

    if replace:
        return [pattern.format(**replace)[:max_len]]
    else:
        return [value[:max_len]]
