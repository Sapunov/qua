import logging

from django.conf import settings

from search import elasticsearch
from search import misc
from search.engine import snippets
from search.engine import utils
from search.engine.translation import translate


esclient = elasticsearch.get_client()

log = logging.getLogger(settings.APP_NAME + '.' + __name__)


class SearchHit:
    '''Only one search result - hit'''

    def __init__(
        self, item_id, ext_id, title, keywords, is_external, resource,
        score, type_, loc, snippet
    ):

        # Internal fields
        self._item_id = item_id
        self._score = score
        self._type = type_
        self._loc = loc

        self.ext_id = ext_id
        self.title = title
        self.keywords = keywords
        self.is_external = is_external
        self.resource = resource
        self.snippet = snippet
        self.image = None


class SearchResults:
    '''Create a list of search results'''

    def __init__(
            self, query, total, results=None,
            suggested_query=None, query_words=None):

        self.query = query
        self.suggested_query = suggested_query

        self.total = total
        self.hits = []
        self.max_score = results[0][0] if self.total > 0 else 0
        self.min_score = results[0][0] if self.total > 0 else 0

        if self.total > 0:
            for score, item_id, source in results:
                self.max_score = max(self.max_score, score)
                self.min_score = min(self.min_score, score)

                self.hits.append(
                    SearchHit(
                        item_id,
                        source['ext_id'],
                        source['title'],
                        source['keywords'],
                        source['is_external'],
                        source['resource'],
                        score,
                        source.get('_type', settings.MAIN_SEARCH_SERVICE_NAME),
                        source.get('_loc', settings.MAIN_SEARCH_SERP_LOCATION),
                        snippets.generate_snippet(source['text'], query_words)
                    )
                )


def es_spelling_correction(
        query,
        index=settings.ES_SPELLING_INDEX,
        field='text'
):
    '''Trying to correct only one word in user query.

    Gets a user query and return query with only 1 corrected word if it exists.
    '''

    corrected = False
    corrected_word = None
    # Now it is a list but we return string by joining list items
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

    log.debug('Answer from elasticsearch suggest by query body: %s: %s',
              body, result)

    # Funny thing: when es index has no items .suggest method returns dict
    # without any field (`spelling` in this case) but when index not empty and
    # there is not suggestions method returns dict with `spelling` field
    if 'spelling' in result:
        for suggest in result['spelling']:
            # Only first corrected word makes sense. All words after
            # first corrected appends as they are in user query.
            if suggest['options'] and not corrected:
                corrected = True
                # As a second param we use first ES.SEGGEST option because
                # this option has highest score
                output.append(suggest['options'][0]['text'])

                # We cannot highlight corrected word here but we should do it
                # in future, corrected_word = word to highlight
                corrected_word = output[-1]
            else:
                output.append(suggest['text'])

    log.debug('Query after typos correction: %s', output)

    return (corrected, ' '.join(output), corrected_word)


def check_keyboard_layout_error(query):
    '''Trying to determine whether user query makes sense.

    Function counts number of results for user query and keyboard layout
        inverted user query and make decision based on counts.
    '''

    get_query = lambda query: {'query': utils.multimatch_builder(query)}

    corrected = False
    inverted_query = misc.keyboard_layout_inverse(query)

    count_query, *_ = utils.search_query(get_query(query))
    count_inverted_query, *_ = utils.search_query(get_query(inverted_query))

    log.debug('Normal query results - %s, inverted_layout results - %s',
              count_query, count_inverted_query)

    if not count_query and count_inverted_query:
        corrected = True
        query = inverted_query

    return (corrected, query)


def spelling_correction(query):
    '''Trying to make 2 types of spelling correction:
        - keyboard inverse
        - typos

    Returns: tuple - (whether query corrected, corrected_query, corrected_word)
    '''

    # First: check keyboard layout
    corrected, corrected_query = check_keyboard_layout_error(query)

    if corrected:
        return (True, corrected_query, None)

    # Second: check for typos
    corrected, corrected_query, corrected_word = es_spelling_correction(query)

    if corrected:
        return (True, corrected_query, corrected_word)

    # If query OK return it as it is
    return (False, None, None)


def extend_query(query):
    '''Returns list of lists with extended words for every word in query.
    '''

    words = query.split(' ')
    output = []

    for word in words:
        temp = [word]

        translation = translate(word)
        log.debug('Translation of %s : %s', word, translation)

        if translation:
            temp.append(translation)

        output.append(misc.delete_duplicates(temp))

    return output


def create_query(words):
    '''Create query in form of ES syntax.'''

    must = []

    for terms in words:
        must.append(utils.multimatch_builder(' '.join(terms)))

    query = utils.create_boolean_query(must, policy='must')

    # TODO: make code below as a separate function
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


def search_items(query, limit, offset, spelling=True):
    '''Main search functions for calling from any place.'''

    log.debug('User query: %s, limit=%s, offset=%s, spelling=%s',
              query, limit, offset, spelling)

    query = utils.preprocess_user_query(query)

    log.debug('Query after first preprocessing: %s', query)

    corrected = False
    corrected_query = None

    if spelling:
        corrected, corrected_query, corrected_word = spelling_correction(query)

        log.debug('Spelling activated. Was query corrected: %s, ' \
                  'corrected query: %s, corrected_word: %s',
                  corrected, corrected_query, corrected_word)

    words = extend_query(corrected_query if corrected else query)

    log.debug('Words with extended query: %s', words)

    es_query = create_query(words)

    log.debug('Elasticsearch query: %s', es_query)

    total, _, results = utils.search_query(es_query, size=limit, from_=offset)

    log.debug('Total results found: %s, results: %s', total, results)

    # Before send to user we need to highlight wrong word(s)
    if corrected:
        corrected_query = utils.highlight_words(corrected_query, corrected_word)
        log.debug('Highlighted corrected query: %s', corrected_query)

    return SearchResults(query, total, results, corrected_query, words)
