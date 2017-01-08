import logging

from django.utils import timezone

from qua import utils
from qua.api.models import SearchHistory, Questions
from qua.api.exceptions import ExitDecoratorError


log = logging.getLogger('qua.' + __name__)


def get_object(obj, primary_key):
    try:
        return obj.objects.get(pk=primary_key)
    except obj.DoesNotExist:
        raise ExitDecoratorError('Item with pk={0} not found in {1}'.format(
            primary_key, obj))


def search_tracker(params):
    if 'shid' in params:
        shid = params['shid']
    else:
        raise ExitDecoratorError('Shid not specified')

    if 'qid' in params:
        qid = params['qid']
    else:
        raise ExitDecoratorError('Qid not specofied')

    if ('token' not in params) or (
        not utils.is_sign_ok(params['token'], '{0}-{1}'.format(shid, qid))
    ):
        raise ExitDecoratorError('Wrong token or not specified')

    history_record = get_object(SearchHistory, shid)

    if history_record.clicked_at is None:
        question = get_object(Questions, qid)

        history_record.question = question
        history_record.clicked_at = timezone.now()
        history_record.save()


def trackable(func):
    def wrapper(self, request, *args, **kwargs):
        params = request.GET

        if 'track' in params:
            try:
                if params['track'] == 'search':
                    search_tracker(params)
            except ExitDecoratorError as exc:
                log.debug(exc)
                return func(self, request, *args, **kwargs)

        return func(self, request, *args, **kwargs)
    return wrapper
