from django.utils import timezone
from django.db import models

from qua import constants


class AccumulateQueue(models.Model):

    text = models.CharField(max_length=300)
    last = models.IntegerField(default=-1)
    quick_ans = models.CharField(max_length=300, blank=True, null=True)
    freq = models.IntegerField(default=1)
    processed = models.BooleanField(default=False)
    group_id = models.CharField(max_length=14)

    @classmethod
    def add(cls, items):

        group_id = timezone.now().strftime(constants.DT_ID_FORMAT)

        for item in items:
            to_add = {
                'text': item['text'],
                'last': item.get('last'),
                'quick_ans': item.get('quick_ans'),
                'freq': item.get('freq'),
                'group_id': group_id
            }

            # Not history data hasn't got last field -> -1
            # If `last` = 0 -> 1 to avoid division by zero
            if to_add['last'] is None:
                del to_add['last']
            elif to_add['last'] <= 0:
                to_add['last'] = 1

            if to_add['quick_ans'] is None:
                del to_add['quick_ans']

            if to_add['freq'] is None:
                del to_add['freq']

            try:
                cls.objects.create(**to_add)
            except Exception:
                continue
