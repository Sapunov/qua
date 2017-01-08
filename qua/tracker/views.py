import logging

from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone

from qua import utils
from qua.api.models import SearchHistory, Questions


log = logging.getLogger('qua.' + __name__)


def get_object(obj, primary_key):
    try:
        return obj.objects.get(pk=primary_key)
    except obj.DoesNotExist:
        raise Http404


def search_tracker(request):
    params = request.GET

    if 'shid' in params:
        shid = params['shid']
    else:
        log.debug('`Shid` is not specified')
        raise Http404

    if 'qid' in params:
        qid = params['qid']
    else:
        log.debug('`qid` is not specified')
        raise Http404

    if ('token' not in params) or (
        not utils.is_sign_ok(params['token'], '{0}-{1}'.format(shid, qid))
    ):
        log.debug('Wrong token or not specified')
        raise Http404

    history_record = get_object(SearchHistory, shid)

    if history_record.clicked_at is None:
        question = get_object(Questions, qid)

        history_record.question = question
        history_record.clicked_at = timezone.now()
        history_record.save()

    if 'redirect' in params:
        return redirect(params['redirect'])
    else:
        return redirect('/')
