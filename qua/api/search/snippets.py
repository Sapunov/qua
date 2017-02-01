import re
import logging


log = logging.getLogger('qua.' + __name__)


def _create_dict_key(word):

    extracted = re.findall(r"(\w+)", word, re.UNICODE)

    if not extracted:
        return None
    else:
        return extracted[0].lower()


def _words_mappings(text):

    words_map = {}
    list_of_words = []

    sum_of_words_len = 0

    for idx, word in enumerate(text.split(' ')):
        sum_of_words_len += len(word)

        list_of_words.append(word)

        dict_item = _create_dict_key(word)

        if dict_item is None:
            continue

        if dict_item not in words_map:
            words_map[dict_item] = [idx]
        else:
            words_map[dict_item].append(idx)

    avg_word_len = sum_of_words_len / len(list_of_words)

    return words_map, list_of_words, avg_word_len


def _get_surround(list_of_words, item_id, left=2, right=2):

    tail = len(list_of_words) - 1

    if 0 > item_id > tail:
        return []

    result = []

    for i in range(item_id - left, item_id + (right + 1)):
        try:
            result.append(list_of_words[i])
        except IndexError:
            continue

    return result


def _generate_phrases_ids(mapping, merged):

    pos = None
    result = []
    tmp = []

    for i in merged:
        if pos is None:
            pos = mapping[i] + 1
            tmp.append(i)
            continue

        if mapping[i] != pos:
            result.append(tmp)
            pos = mapping[i] + 1
            tmp = [i]
        else:
            pos += 1
            tmp.append(i)

    result.append(tmp)

    return sorted(result, key=lambda x: len(x), reverse=True)


def _calc_word_per_term(query_terms_count, snippet_len, avg_word_len):

    avg_word_len = avg_word_len or 1

    return int(snippet_len / query_terms_count / avg_word_len)


def _highlight_snippet(snippet_list, query_terms, html_tag='strong'):

    result = []

    for snippet_item in snippet_list:
        for word in snippet_item:
            if _create_dict_key(word) in query_terms:
                result.append('<{0}>{1}</{0}>'.format(html_tag, word))
            else:
                result.append(word)

        result.append('...')

    return ' '.join(result)


def _parse_query(query, words_map):

    list_of_terms = [it.lower() for it in query.split(' ')]
    mapping = {}
    merged = []

    for idx, term in enumerate(list_of_terms):
        if term in words_map:
            for term_id in words_map[term]:
                mapping[term_id] = idx

            merged.extend(words_map[term])

    return mapping, tuple(sorted(merged))


def generate_snippet(text, query, length=200):

    words_map, list_of_words, avg_word_len = _words_mappings(text)
    snippet_items = []
    mapping, merged = _parse_query(query, words_map)
    phrases_ids = _generate_phrases_ids(mapping, merged)

    query_terms = re.findall(r"(\w+)", query, re.UNICODE)

    words_coef = int(_calc_word_per_term(len(query_terms), length, avg_word_len) / 2)

    overall_snippet_len = 0

    for item in phrases_ids:
        tmp = []

        if len(item) > 1:
            for i, idx in enumerate(item):
                if i == 0:
                    tmp.extend(_get_surround(list_of_words, idx, left=words_coef, right=0))
                elif i == len(item) - 1:
                    tmp.extend(_get_surround(list_of_words, idx, left=0, right=words_coef))
                else:
                    tmp.extend(list_of_words[idx])
        else:
            try:
                tmp = _get_surround(list_of_words, item[0], left=words_coef, right=words_coef)
            except IndexError:
                continue

        snippet_items.append(tmp)

        overall_snippet_len += sum([len(it) for it in tmp])

        if overall_snippet_len > length:
            break

        tmp = []

    return _highlight_snippet(snippet_items, query_terms)
