import requests
import logging


log = logging.getLogger('qua.' + __name__)


def download_image(image_url):
    pass


def retrieve_page(url):

    log.debug('Trying to retieve page: %s', url)

    try:
        r = requests.get(url, timeout=30)
    except requests.exceptions.RequestException as e:
        log.exception('Exception while retrieving %s: %s', url, e)

        return None

    if r.status_code == 200:
        return r.text
