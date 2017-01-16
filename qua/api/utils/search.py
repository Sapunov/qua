import re
import json
import logging

from django.conf import settings
import xapian


log = logging.getLogger('qua.' + __name__)


def glue_text(text):

    return ''.join(re.findall(r"(\w+)", text, re.UNICODE))


def avg(*args):

    return sum(args) / len(args)


def is_english(text):

    count_ascii = 0
    text_line = glue_text(text)

    for char in text_line:
        if ord(char) < 128:
            count_ascii += 1
        else:
            count_ascii -= 1

    return count_ascii >= 0


def get_queryparser(query):

    queryparser = xapian.QueryParser()

    lang = 'en' if is_english(query) else 'ru'

    log.debug('Query language: %s' % lang)

    queryparser.set_stemmer(xapian.Stem(lang))

    queryparser.set_stemming_strategy(queryparser.STEM_ALL)
    queryparser.set_default_op(xapian.Query.OP_OR)

    return queryparser


def search(querystring):

    db = xapian.Database(settings.SEARCH_INDEX_DB)

    queryparser = get_queryparser(querystring)

    query = queryparser.parse_query(querystring)

    log.debug('Parsed query: %s', query)

    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    match_set = enquire.get_mset(0, settings.SEARCH_RESULTS_MAX)

    merged = {}

    for match in match_set:
        data = json.loads(match.document.get_data().decode('utf8'))

        if data['id'] not in merged:
            merged[data['id']] = {
                'id': match.docid,
                'score': match.percent,
                'text': data['text']
            }
        else:
            merged[data['id']]['score'] = avg(
                merged[data['id']]['score'],
                match.percent
            )

    output = {
        'total': match_set.get_matches_estimated() / 2,
        'hits': merged
    }

    return output
