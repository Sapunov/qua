import re
import logging

import lxml.html
from bs4 import BeautifulSoup

from qua.api.search.engine import get_search_engine
from qua.api.search.snippets import Snipper


log = logging.getLogger('qua.' + __name__)


def delete_tags(soup_instance, tags):

    if isinstance(tags, str):
        tags = (tags,)

    for tag in tags:
        try:
            _ = [item.extract() for item in soup_instance(tag)]
        except TypeError:
            continue

    return soup_instance


def deduplicate_spaces(text):

    return re.sub('(\s|\\n)+', ' ', text).strip()


def get_title(html):

    if html == '':
        return html

    soup = BeautifulSoup(html, 'lxml')

    title = soup.title

    if title is not None:
        return title.get_text()
    else:
        return ''


def get_text_from_html(html):

    if html == '':
        return html

    soup = BeautifulSoup(html, 'lxml')

    if soup.body is not None:
        body = delete_tags(soup.body, ('script', 'style', 'noscript'))
        text = deduplicate_spaces(body.get_text())
    else:
        text = ''

    return text


def extract_all_links(html):

    if html == '':
        return []

    html = lxml.html.fromstring(html)
    links = set(html.xpath("//a/@href"))

    return links


def get_spelling_text(title, keywords, text, external, external_content):

    result = ''

    if title:
        result += title + ' '

    if text:
        result += text + ' '

    if external:
        result += external + ' '

    if external_content:
        result += external_content + ' '

    if keywords:
        result += ' '.join(keywords)

    return result.strip()


def spelling_correction(query, index='_all', field='spelling'):

    engine = get_search_engine()

    corrected = False
    output = ''
    body = {
        'spelling': {
            'text': query,
            'term': {
                'field': field
            }
        }
    }

    result = engine.suggest(index=index, body=body)

    for suggest in result['spelling']:
        if len(suggest['options']) > 0:
            corrected = True
            output += suggest['options'][0]['text'] + ' '
        else:
            output += suggest['text'] + ' '

    return (corrected, output.strip())


def translit(string):

    dic = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ь': '',
        'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'ju', 'я': 'ja', 'a': 'а', 'b': 'б',
        'c': 'ц', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и',
        'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
        'q': 'q', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'v': 'в', 'w': 'w',
        'x': 'x', 'y': 'ы', 'z': 'з'
    }

    result = ''

    for letter in string:
        result += dic.get(letter, letter)

    return result


def keyboard_layout_inverse(string):
    dic = {
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u',
        'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's',
        'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l',
        'ж': ';', 'э': '\'', 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b',
        'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.', 'ё': '`', 'q': 'й', 'w': 'ц',
        'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ',
        'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а',
        'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', '\'': 'э',
        'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь',
        ',': 'б', '.': 'ю', '`': 'ё'
    }

    result = ''

    for letter in string:
        result += dic.get(letter, letter)

    return result


def generate_snippet(query, hit):

    text = hit.get('text')

    if text is None:
        text = hit.get('external_content')

    if text is None:
        return ''

    snipper_obj = Snipper(text)

    return snipper_obj.generate_snippet(query, 200)
