import re
import logging


log = logging.getLogger('qua.' + __name__)


class Snipper:

    def __init__(self, text):

        self._words = {}
        self.list_of_words = []
        self.avg_word_len = 0

        counter = -1
        sum_of_words_len = 0

        for item in text.split(' '):
            sum_of_words_len += len(item)

            self.list_of_words.append(item)
            counter += 1

            dict_item = self._process_word(item)

            if dict_item is None:
                continue

            if dict_item not in self._words:
                self._words[dict_item] = [counter]
            else:
                self._words[dict_item].append(counter)

        self.avg_word_len = sum_of_words_len / len(self.list_of_words)

    def _process_word(self, word):

        extracted = re.findall(r"(\w+)", word, re.UNICODE)

        if not extracted:
            return None
        else:
            return extracted[0].lower()


    def __str__(self):

        return '<Words:%s>' % len(self._words)

    def __repr__(self):

        return self.__str__()

    def _parse_query(self, query):

        list_of_terms = [it.lower() for it in query.split(' ')]
        mapping = {}
        merged = []

        for idx, term in enumerate(list_of_terms):
            if term in self._words:
                for term_id in self._words[term]:
                    mapping[term_id] = idx

                merged.extend(self._words[term])

        return mapping, tuple(sorted(merged))

    def _get_surround(self, item_id, left=2, right=2):

        tail = len(self.list_of_words) - 1

        if 0 > item_id > tail:
            return []

        result = []

        for i in range(item_id - left, item_id + (right + 1)):
            try:
                result.append(self.list_of_words[i])
            except IndexError:
                continue

        return result

    def _generate_phrases_ids(self, mapping, merged):

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

    def _calc_word_per_term(self, query_terms_count, snippet_length):

        return int(snippet_length / query_terms_count / self.avg_word_len)

    def _highlight_snippet(self, snippet_list, query_terms, html_tag='strong'):

        result = []

        for snippet_item in snippet_list:
            for word in snippet_item:
                if self._process_word(word) in query_terms:
                    result.append('<{0}>{1}</{0}>'.format(html_tag, word))
                else:
                    result.append(word)

            result.append('...')

        return ' '.join(result)

    def generate_snippet(self, query, length=200):

        snippet_items = []
        mapping, merged = self._parse_query(query)
        phrases_ids = self._generate_phrases_ids(mapping, merged)

        query_terms = re.findall(r"(\w+)", query, re.UNICODE)

        words_coef = int(self._calc_word_per_term(len(query_terms), length) / 2)

        overall_snippet_len = 0

        for item in phrases_ids:
            tmp = []

            if len(item) > 1:
                for i, idx in enumerate(item):
                    if i == 0:
                        tmp.extend(self._get_surround(idx, left=words_coef, right=0))
                    elif i == len(item) - 1:
                        tmp.extend(self._get_surround(idx, left=0, right=words_coef))
                    else:
                        tmp.extend(self.list_of_words[idx])
            else:
                try:
                    tmp = self._get_surround(item[0], left=words_coef, right=words_coef)
                except IndexError:
                    continue

            snippet_items.append(tmp)

            overall_snippet_len += sum([len(it) for it in tmp])

            if overall_snippet_len > length:
                break

            tmp = []

        return self._highlight_snippet(snippet_items, query_terms)
