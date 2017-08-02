'''QUA miscellaneous functions'''


def int2hex_id(integer):
    '''Converts int to service specific identifier format'''

    return hex(integer)[2:].zfill(8)


def hex_id2int(hex_id):
    '''Converts service specific identifier format to int'''

    return int(hex_id, 16)


def delete_duplicates(list_of_items):
    '''Returns list with unique items of list_of_items.'''

    return list(set(list_of_items))


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
