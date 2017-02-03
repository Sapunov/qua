import logging

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import exceptions

from qua.api.search.engine import get_search_engine
from qua.api.search.engine import exceptions as es_exceptions
from qua.api.search import utils
from qua.api.search import crawler
from qua.api.models import ExternalResource


log = logging.getLogger('qua.' + __name__)


def _index(
    resource_id, title, is_external=False, text=None, keywords=None, url=None,
    external_content=None
):

    engine = get_search_engine()

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
    except es_exceptions.ElasticsearchException as e:
        log.exception('ElasticsearchException: %s', e)


def index_external_resource(url):

    log.debug('Index external resource: %s', url)

    god_user = User.objects.get(username='god')
    external_resource, created = ExternalResource.create(url, god_user)

    if not created:

        log.debug('External resource already created')

        try:
            content = external_resource.get_content()
            return content if content is not None else ''
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
