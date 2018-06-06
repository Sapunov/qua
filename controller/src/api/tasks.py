'''Tasks for rq worker'''

import logging

from django.conf import settings

from api import misc
from api import models
from api import retriever
from api import search


log = logging.getLogger(settings.APP_NAME + __name__)


def index_external_resources(link_or_links, user=None):
    '''Index extrnal resources'''

    # Ensure list of links
    if isinstance(link_or_links, str):
        links = [link_or_links]
    else:
        links = link_or_links

    for url in links:
        url = misc.normalize_url(url)
        ext_resource, created = models.ExternalResource.create(url, user)

        log.debug('%s. Was created: %s', ext_resource, created)

        if created or ext_resource.se_id is None:
            if not ext_resource.index_resource():
                log.error('Cannot index external resource. Deleting...')
                ext_resource.delete()


def index_question(question_obj):
    '''Index question within search microservice'''

    if not question_obj.answer_exists:
        log.debug('%s have no answer and will not be sent', question_obj)
        return None

    html = question_obj.answer.html
    text = misc.html2text(html)['text']

    item_id = search.index_item(
        question_obj.id,
        question_obj.title,
        text,
        keywords=question_obj.get_keywords_text_only())

    # set external search engine id
    question_obj.se_id = item_id
    question_obj.save()

    # INDEX EXTERNAL
    links = misc.extract_all_links(html)
    if links:
        index_external_resources(links)


def reindex_question(question_obj):
    '''Send question data to search microservice to update some fields'''

    # If user add answer
    if question_obj.se_id is None:
        return index_question(question_obj)

    # if user delete item
    if not question_obj.answer_exists and question_obj.se_id is not None:
        search.delete_item(question_obj.se_id)
    else:
        html = question_obj.answer.html
        text = misc.html2text(html)['text']

        search.update_item(
            question_obj.se_id,
            question_obj.title,
            text,
            keywords=question_obj.get_keywords_text_only())

        # INDEX EXTERNAL
        links = misc.extract_all_links(html)
        if links:
            index_external_resources(links)


def delete_from_index(question_obj):
    '''Delete question from search index'''

    item_id = question_obj.se_id

    if item_id is not None:
        search.delete_item(item_id)


def update_external_resources():
    '''Update all external resources by update_interval'''

    resources = models.ExternalResource.objects.all()

    log.debug('There is %s resources to update', resources.count())

    for resource in resources:
        log.debug('Need to update %s: %s', resource, resource.need_update)

        if resource.need_update:
            resource.index_resource()
