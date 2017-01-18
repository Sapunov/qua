import json
import string

from nltk.tokenize import word_tokenize
from django.conf import settings
import xapian


def tokenize(text, to_lower=True):

    tokens = word_tokenize(text)

    if to_lower:
        tokens = map(lambda t: t.lower(), tokens)

    return filter(lambda t: t not in string.punctuation, tokens)


def word_delimiter(word, min_length=3):

    word_len = len(word)

    if word_len <= min_length:
        return [word]
    else:
        words = []
        for i in range(min_length, word_len + 1):
            words.append(word[:i])

    return words


def process_text(text):

    tokens = tokenize(text)
    result = []

    for token in tokens:
        result.extend(word_delimiter(token))

    return ' '.join(result)


def get_termgenerator(lang):

    termgen = xapian.TermGenerator()
    termgen.set_stemmer(xapian.Stem(lang))

    return termgen


def get_database():

    return xapian.WritableDatabase(
        settings.SEARCH_INDEX_DB, xapian.DB_CREATE_OR_OPEN
    )


def index(data):
    """Index data for search

    :data: dictionary with fields:
        - id (primary_key in django database)
        - keywords (string with comma-separated values)
        - text
    """

    database = get_database()

    identifier = data.get('id')
    keywords = process_text(data.get('keywords'))
    text = process_text(data.get('text'))

    for language in settings.SEARCH_LANGUAGES:
        termgenerator = get_termgenerator(language)

        doc = xapian.Document()
        termgenerator.set_document(doc)

        termgenerator.index_text(keywords)
        termgenerator.increase_termpos()
        termgenerator.index_text(text)

        doc.set_data(json.dumps(data))

        idterm = 'Q' + str(identifier) + language
        doc.add_boolean_term(idterm)
        database.replace_document(idterm, doc)
