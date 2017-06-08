import logging
import json
import time

from django.conf import settings

from qua import elasticsearch
from qua import misc
from qua import settings as qua_settings
from qua.search import snippets
from qua.search import utils
from qua.search.stopwords import STOPWORDS
from qua.translation import translate


esclient = elasticsearch.get_client()

log = logging.getLogger(settings.APP_NAME + '.' + __name__)


class SearchHit:

    def __init__(
        self, item_id, ext_id, title, keywords, is_external, resource,
        score, snippet=None
    ):

        self.item_id = item_id
        self.ext_id = ext_id
        self.title = title
        self.keywords = keywords
        self.is_external = is_external
        self.resource = resource
        self.score = score
        self.snippet = snippet
        self.image = None


class SearchResults:

    def __init__(
            self, query, total, took, results=None,
            suggested_query=None, query_words=None):

        start = time.time()

        self.query = query
        self.suggested_query = suggested_query

        self.total = total
        self.hits = []

        if self.total > 0:
            for score, item_id, source in results:
                self.hits.append(
                    SearchHit(
                        item_id,
                        source['ext_id'],
                        source['title'],
                        source['keywords'],
                        source['is_external'],
                        source['resource'],
                        score,
                        snippets.generate_snippet(source['text'], query_words)
                    )
                )

        self.took = round((took + (time.time() - start)) / 1000, 3)


def spelling_correction(
        query, index=qua_settings.ES_SPELLING_INDEX, field='text'):

    query = query.strip().lower()

    corrected = False
    output = []
    body = {
        'spelling': {
            'text': query,
            'term': {
                'field': field
            }
        }
    }

    result = esclient.suggest(index=index, body=body)

    for suggest in result['spelling']:
        if len(suggest['options']) > 0 and not corrected:
            corrected = True
            output.append([suggest['text'], suggest['options'][0]['text']])
        else:
            output.append([suggest['text']])

    return (corrected, output)


def get_suggested_query(words, highlight=True):

    res = []

    for i in range(len(words)):
        if len(words[i]) == 2:
            if highlight:
                res.append('<em>{0}</em>'.format(words[i][1]))
            else:
                res.append(words[i][1])
        else:
            res.append(words[i][0])

    return ' '.join(res)


def extend_query(words):

    for i in range(len(words)):
        # if spelling correction
        if len(words[i]) == 2:
            word = words[i][1]
        else:
            word = words[i][0]

        if word in STOPWORDS:
            words[i] = None
            continue

        words[i].append(misc.keyboard_layout_inverse(word))
        words[i].append(misc.translit(word))

        trans = translate(word)
        if trans:
            words[i].append(trans)

        words[i] = list(set(words[i]))

    return [w for w in words if w is not None]


def create_query(words):

    must = []

    for terms in words:
        must.append({
            'multi_match': {
                'query': ' '.join(terms),
                'fields': qua_settings.SEARCH_FIELDS,
                'operator': 'or'
            }
        })

    query = utils.boolean_query(must, policy='must')

    func_query = {
        'query': {
            'function_score': {
                'query': query,
                'functions': [
                    {
                        'filter': {'match': {'is_external': True}},
                        'weight': 0.5,
                    }
                ]
            }
        }
    }

    return func_query


def search_items(query, limit, offset):

    log.debug('Query: %s', query)

    # And first processing here too
    corrected, words = spelling_correction(query)

    if corrected:
        suggested_query = get_suggested_query(words)
    else:
        suggested_query = None

    words = extend_query(words)
    es_query = create_query(words)

    log.debug('ES query: %s', json.dumps(es_query, indent=2))

    total, took, results = utils.query(
        index=qua_settings.ES_SEARCH_INDEX,
        doc_type=qua_settings.ES_DOCTYPE,
        body=es_query,
        size=limit, from_=offset)

    return SearchResults(query, total, took, results, suggested_query, words)
