import logging

from django.conf import settings

from qua import elasticsearch
from qua import settings as qua_settings
from qua.search import utils


esclient = elasticsearch.get_client()

log = logging.getLogger(settings.APP_NAME + __name__)
