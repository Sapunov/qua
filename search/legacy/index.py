import logging

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import exceptions

from qua.api.search.engine import SearchEngine
from qua.api.search.engine import exceptions as engine_exceptions
from qua.api.search import utils
from qua.api.search import crawler
from qua.api.models import ExternalResource


log = logging.getLogger('qua.' + __name__)


def _add_to_spelling_database(title, text, keywords):

    engine = SearchEngine()

    data = title + ' ' + text
    data = data + ' ' + ' '.join(keywords)

    body = {
        'text': data
    }

    try:
        engine.index(
            index=settings.SEARCH_SPELLING_INDEX_NAME,
            doc_type=settings.SEARCH_SPELLING_INDEX_TYPE,
            body=body
        )
    except engine_exceptions.ElasticsearchException:
        pass


def _index(
    resource_id, title, is_external=False, text=None, keywords=None, url=None,
    external_content=None
):

    engine = SearchEngine()

    data = {
        'title': title,
        'keywords': keywords or [],
        'text': text,
        'external_content': external_content,
        'is_external': is_external,
        'url': url
    }

    try:
        engine.index(
            index=settings.SEARCH_INDEX_NAME,
            doc_type=settings.SEARCH_INDEX_TYPE,
            id=resource_id,
            body=data
        )
    except engine_exceptions.ElasticsearchException:
        pass

    _add_to_spelling_database(title, text, data['keywords'])


def index_external_resource(url):

    log.debug('Index external resource: %s', url)

    god_user = User.objects.get(username='god')
    external_resource, created = ExternalResource.create(url, god_user)

    if not created:

        log.debug('External resource already created')

        try:
            content = external_resource.get_content(fields=('title',))
            return content['title']
        except exceptions.NotFound:
            pass

    html = crawler.retrieve_page(url)

    if html is None:
        external_resource.delete()
        return ''

    title = utils.get_title_from_html(html)
    text = utils.get_text_from_html(html)

    _index('e-%s' % external_resource.id, title,
        is_external=True,
        text=text,
        url=url
    )

    return title


def index_question(question_id, title, keywords, html):

    log.debug('Indexing question %s', question_id)

    text = utils.get_text_from_html(html)
    external_content = ''

    for link in utils.extract_all_links(html):
        external_content += index_external_resource(link)

    _index(
        'q-%s' % question_id, title,
        is_external=False,
        text=text,
        external_content=external_content,
        keywords=keywords
    )
