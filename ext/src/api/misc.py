from importlib import import_module
from urllib.parse import urlparse
from urltools import normalize as utool_normalize
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


def url_part(url, part_name):
    '''Returns value of the part_name of the specific url'''

    parsed = urlparse(url)

    if hasattr(parsed, part_name):
        return getattr(parsed, part_name)

    return None


def extract_hostname(url):
    '''Returns value of hostname as part of the specified url'''

    hostname = url_part(url, 'hostname')

    return hostname if hostname else None


def urlsep(url):
    '''Separate url by scheme and hostname with path and query params'''

    scheme = url_part(url, 'scheme')
    hostname = url_part(url, 'hostname')

    return scheme, url[url.index(hostname):]


def ensure_scheme(url, add_scheme='http'):
    '''Add http of user specified scheme if not exist'''

    if not url_part(url, 'scheme'):
        # ensure that url does not start with //
        url = url.lstrip('/')

        url = '{0}://{1}'.format(add_scheme, url)

    return url


def normalize_url(url):
    '''Normalize url'''

    return ensure_scheme(utool_normalize(url))


def is_valid_hostname(hostname):
    '''Checks whether hostname valid or not.

    Ensures that each segment:
     - contains at least one character and a maximum of 63 characters;
     - consists only of allowed characters;
     - doesn't begin or end with a hyphen.

    Reference: https://stackoverflow.com/questions/2532053/validate-a-hostname-string
    '''

    if len(hostname) > 255:
        return False

    # Strip exactly one dot from the right, if present
    if hostname[-1] == ".":
        hostname = hostname[:-1]

    allowed = re.compile(r'(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)

    return all(allowed.match(x) for x in hostname.split("."))


def hostname2camelcase(hostname):
    '''Converts hostname to the camelcase string.

    Example: vk.com -> VkCom
    '''

    domains = hostname.split('.')

    return ''.join(domain.capitalize() for domain in domains)


def removedots(input_string):
    '''Returns input string with removed dots'''

    return ''.join(input_string.split('.'))


def import_module_class(path_to_class):
    '''Import class from any module'''

    module_name, class_name = path_to_class.rsplit('.', 1)

    module = import_module(module_name)

    try:
        class_ = getattr(module, class_name)
    except AttributeError:
        raise ImportError('No class <%s> in %s' % (class_name, module))

    return class_


def truncate_string(string, truncate_len=100,
                    end_msg='...<the rest of the text is truncated>'):
    '''Truncate string i.e. for logging purposes'''

    return '{0}{1}'.format(string[:truncate_len], end_msg)
