import hashlib
import time


def sha1_hash(string):

    return hashlib.sha1(string.encode('utf-8')).hexdigest()


def sign(string, secret_key, length=20):

    return sha1_hash(string + secret_key)[0:length]


def is_sign_ok(input_sign, string, secret_key, length=20):

    return input_sign == sign(string, secret_key, length=length)


def word_normalize(phrase):

    words = [word.strip().lower() for word in phrase.split(' ')]

    return ' '.join([word for word in words if word])


def create_query(query_dict):
    '''Convert dict to the url string after ?.'''

    return '&'.join(['{0}={1}'.format(k, v) for k, v in query_dict.items()])


def time_elapsed(start_time):
    '''This function suggest that start_time is time.time() call'''

    return round(time.time() - start_time, 3)
