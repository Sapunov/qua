import datetime
import os
import pickle

from django.conf import settings

from qua import misc
from suggests.preprocessing import create_tst


TREE = None
REQUESTS_COUNT = 0


class SuggestItem:

    def __init__(self, text, rate, quick_ans, prefix):

        self.text = text
        self.rate = rate
        self.quick_ans = quick_ans
        self.prefix = prefix


def load_or_create():

    # If exists tree file
    if os.path.exists(settings.SUGGESTS_TREE_PATH):
        modif_time = datetime.datetime.now() - datetime.timedelta(
            seconds=settings.SUGGESTS_UPDATE_INTERVAL)

        if TREE is not None and not misc.was_file_modified(
                settings.SUGGESTS_TREE_PATH,
                modif_time,
                raise_exception=False):
            return TREE

        with open(settings.SUGGESTS_TREE_PATH, 'rb') as fd:
            return pickle.load(fd)

    # Create tree if no one create it before
    return create_tst()


def load_tree():

    global TREE, REQUESTS_COUNT

    REQUESTS_COUNT += 1

    if TREE is None \
            or REQUESTS_COUNT > settings.SUGGESTS_REQUEST_UPDATE_INTERVAL:
        REQUESTS_COUNT = 0
        TREE = load_or_create()


def suggest(prefix, limit):

    prefix = prefix.lower()

    ans = []

    load_tree()

    if TREE:
        results = TREE.common_prefix(prefix, limit)

        if not results and len(prefix) > 1:
            prefix = misc.keyboard_layout_inverse(prefix)
            results = TREE.common_prefix(prefix, limit)

        if results:
            for result in results:
                ans.append(
                    SuggestItem(result[1], result[0], result[2], prefix))

    return ans
