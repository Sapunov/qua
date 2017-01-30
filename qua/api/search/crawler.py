import requests


def download_image(image_url):
    pass


def retrieve_page(url):

    try:
        r = requests.get(url)
    except Exception:
        return None

    if r.status_code == 200:
        return r.text
