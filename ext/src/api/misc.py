import hashlib
import lxml.html
import os
import re
import time


def sha1_hash(string):
    '''Returns sha1 hash string created from input string'''

    return hashlib.sha1(string.encode('utf-8')).hexdigest()


def sign(string, secret_key, length=20):
    '''Returns sha1 string hash with the specific length'''

    return sha1_hash(string + secret_key)[0:length]


def is_sign_ok(input_sign, string, secret_key, length=20):
    '''Check whether input_sign coincides with the real sigh'''

    return input_sign == sign(string, secret_key, length=length)


def word_normalize(phrase):
    '''Simple word preprocessing. Strip and lower, no more'''

    words = [word.strip().lower() for word in phrase.split(' ')]

    return ' '.join([word for word in words if word])


def create_query(query_dict):
    '''Convert dict to the url string after ?.'''

    return '&'.join(['{0}={1}'.format(k, v) for k, v in query_dict.items()])


def time_elapsed(start_time):
    '''This function suggest that start_time is time.time() call'''

    return round(time.time() - start_time, 3)


def resolve_dots(url, services_dict):
    '''Search dot separated name in the settings dict.

    For example: services = {
        'search': {
            'main': {
                'host': 'localhost'
            }
        }
    }

    if you call resolve_dots('search_main') this function returns:
        localhost

    '''

    name, path = url.split('/', 1)

    current_value = services_dict

    for part in name.split('.'):
        current_value = current_value[part]

    host = current_value['host']

    return os.path.join(host, path)


def extract_all_links(html, filter_hash=True):
    '''Returns list of all links founded on the html page'''

    if html == '':
        return []

    html = lxml.html.fromstring(html)
    # Extract and deduplicate
    links = list(set(html.xpath("//a/@href")))

    if filter_hash:
        links = [link for link in links if not link.startswith('#')]

    return links


def deduplicate_spaces(text):
    '''Delete repetitive spaces and strip input text'''

    return re.sub(r'(\s)+', ' ', text).strip()


def _html2text(node, forbidden_tags):
    '''Recursively traverse html tree and extract only text not
        allowing words to stick together'''

    text = ''

    if not node.tag in forbidden_tags and \
            not isinstance(node, lxml.html.HtmlComment):
        text = ' %s ' % node.text if node.text else ''

    children = node.getchildren()

    if children:
        for child in children:
            text += ' %s ' % _html2text(child, forbidden_tags)

    return text


def html2text(html, forbidden_tags=('script', 'style', 'noscript', 'img')):
    '''Extract only text from html tags'''

    title = ''
    text = ''

    tree = lxml.html.fromstring(html)

    title_el = tree.find(".//title")
    if title_el is not None:
        title = title_el.text

    # Since the title extracting separately and in `html` may be not only html
    # we process html tree from the very beginning and process title tag too.
    # But there is no need to process title again that is why we need to include
    # title tag in `forbidden_tags`
    if 'title' not in forbidden_tags:
        forbidden_tags += ('title',)

    text = deduplicate_spaces(_html2text(tree, forbidden_tags))

    return {'title': title, 'text': text}
