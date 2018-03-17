import logging

from django.conf import settings

from search import elasticsearch
from search import misc
from search.engine import constants
from search.engine import snippets
from search.engine import utils
# from search.engine.translation import translate


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
        # TODO: убрать поле self.url - используется для поддержки старого SERP
        self.url = resource
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
    query_terms = []
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
                query_terms.append((suggest['text'], suggest['options'][0]['text']))
            else:
                query_terms.append((suggest['text'], None))

    log.debug('Query after typos correction: %s', query_terms)

    return (corrected, query_terms)


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

    query_terms = []

    if not count_query and count_inverted_query:
        corrected = True

        for word in query.split(' '):
            query_terms.append((word, misc.keyboard_layout_inverse(word)))

    return (corrected, query_terms)


def spelling_correction(query):
    '''Trying to make 2 types of spelling correction:
        - keyboard inverse
        - typos

    Returns: tuple - (whether query corrected, corrected_query, corrected_word)
    '''

    # First: check keyboard layout
    corrected, query_terms = check_keyboard_layout_error(query)

    if corrected:
        return (corrected, query_terms, constants.KEYBOARD_LAYOUT_SUGGEST_NAME)

    # Second: check for typos
    corrected, query_terms = es_spelling_correction(query)

    if corrected:
        return (corrected, query_terms, constants.TYPOS_SUGGEST_NAME)

    return (False, None, '')


def extend_query(query_terms):
    '''Returns list of lists with extended words for every word in query.
    '''

    output = []

    for user_word, suggested_word in query_terms:
        temp = [user_word]

        if suggested_word is not None:
            temp.append(suggested_word)

        # translation = translate(user_word)

        # if translation:
        #     temp.append(translation)
        #     log.debug('Translation of %s : %s', word, translation)

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
    suggested_query = None
    query_terms = []

    if spelling:
        corrected, query_terms, correction_type = spelling_correction(query)

        log.debug('Spelling activated. Was query corrected?: %s, ' \
                  'query terms: %s', corrected, query_terms)

    # If not corrected we cannot be sure that query_terms is query terms
    if not corrected:
        query_terms = utils.string2terms(query)

    words = extend_query(query_terms)

    log.debug('Words with extended query: %s', words)

    es_query = create_query(words)

    log.debug('Elasticsearch query: %s', es_query)

    total, _, results = utils.search_query(es_query, size=limit, from_=offset)

    log.debug('Total results found: %s', total)

    # Before send to user we need to highlight wrong word(s)
    if corrected:
        suggested_query = utils.highlight_words(
            query_terms,
            highlight_all=(correction_type == constants.KEYBOARD_LAYOUT_SUGGEST_NAME))

        log.debug('Highlighted corrected query: %s', suggested_query)

    return SearchResults(query, total, results, suggested_query, words)
