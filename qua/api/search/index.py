import logging

from django.conf import settings

from qua.api.search.engine import get_search_engine
from qua.api.search import utils


log = logging.getLogger('qua.' + __name__)


def index_external_resource(url, question_id=None):

    log.debug('Index external resource: %s on question %s', url, question_id)

    return ''


def index_question(question_id, title, keywords, html):

    log.debug('Indexing question %s', question_id)

    engine = get_search_engine()

    text = utils.get_text_from_html(html)
    external = ''

    for link in utils.extract_all_links(html):
        external += index_external_resource(link, question_id)

    spelling = utils.get_spelling_text(title, keywords, text, external)

    data = {
        'title': title,
        'keywords': keywords,
        'text': text,
        'external': external,
        'spelling': spelling,
        'is_external': False
    }

    engine.index(
        index=settings.SEARCH_INDEX_NAME,
        doc_type=settings.SEARCH_INDEX_TYPE,
        id='q-%s' % question_id,
        body=data
    )
