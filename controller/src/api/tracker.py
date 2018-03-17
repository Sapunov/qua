import logging

from django.conf import settings
from django.utils import timezone

from api import misc
from app.exceptions import ExitDecoratorError
from api.models import SearchHistory, Question, ExternalResource


log = logging.getLogger(settings.APP_NAME + __name__)


def get_object(obj, primary_key):

    try:
        return obj.objects.get(pk=primary_key)
    except obj.DoesNotExist:
        raise ExitDecoratorError('Item with pk={0} not found in {1}'.format(
            primary_key, obj))


def search_tracker(params, external=False):

    if 'shid' in params:
        shid = params['shid']
    else:
        raise ExitDecoratorError('Shid not specified')

    if 'qid' in params:
        qid = params['qid']
    else:
        raise ExitDecoratorError('Qid not specofied')

    if ('token' not in params) or (
        not misc.is_sign_ok(
            params['token'], '{0}-{1}'.format(shid, qid), settings.SECRET_KEY)
    ):
        raise ExitDecoratorError('Wrong token or not specified')

    history_record = get_object(SearchHistory, shid)

    if history_record.clicked_at is None:
        if external:
            external_resource = get_object(ExternalResource, qid)
            history_record.external_resource = external_resource
            history_record.external = True
        else:
            question = get_object(Question, qid)
            history_record.question = question

        history_record.clicked_at = timezone.now()
        history_record.save()


# TODO: make in decorator better with functools
def trackable(func):

    def wrapper(self, request, *args, **kwargs):

        params = request.GET

        if 'track' in params:
            try:
                if params['track'] == 'search_internal':
                    search_tracker(params)
                elif params['track'] == 'search_external':
                    search_tracker(params, external=True)
            except ExitDecoratorError as exc:
                log.debug(exc)
                return func(self, request, *args, **kwargs)

        return func(self, request, *args, **kwargs)

    return wrapper
