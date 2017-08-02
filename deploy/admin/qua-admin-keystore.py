#!/usr/bin/env python3

import argparse
import os
import random
import string
import sys


STORAGE_DIR = '/var/lib/qua/deployment-tool'
DJANGO_KEY = os.path.join(STORAGE_DIR, 'djangokey')
DB_KEY = os.path.join(STORAGE_DIR, 'dbkey')


if not os.path.exists(STORAGE_DIR):
    print('Please, create directory: `{0}` before using this tool'.format(
        STORAGE_DIR))
    sys.exit(1)


def _save_content(content, filename):

    with open(filename, 'w') as opened_file:
        opened_file.write(content)

    return True


def _read_content(filename):

    with open(filename) as opened_file:
        return opened_file.read()


def _generate_django_key():

    chars = string.ascii_letters
    chars += string.digits
    chars += '!#$%&()*+,-.:;<=>?@[]^_`{|}~'

    return ''.join(random.SystemRandom().choice(chars) for _ in range(50))


def djangokey(args):

    if args.regen or not os.path.exists(DJANGO_KEY):
        key = _generate_django_key()
        _save_content(key, DJANGO_KEY)
    else:
        key = _read_content(DJANGO_KEY)

    return key


def dbkey(args):

    if args.set:
        _save_content(args.set, DB_KEY)
        return "OK"

    if os.path.exists(DB_KEY):
        return _read_content(DB_KEY)
    else:
        print('ERROR: dbkey not specified!')
        sys.exit(1)


def get_parser():

    parser = argparse.ArgumentParser(description='QUA deployment tool')
    subparsers = parser.add_subparsers(help='commands', dest='subparser_name')

    # command
    djangokey_parser = subparsers.add_parser(
        'djangokey', help='Get django secret key for service deployment')
    djangokey_parser.add_argument(
        '--regen',
        action='store_true', default=False, help='Create new key if old exists')
    djangokey_parser.set_defaults(func=djangokey)

    # command
    dbkey_parser = subparsers.add_parser(
        'dbkey', help='Get database key for service deployment')
    dbkey_parser.add_argument('--set', type=str, help='Set password')
    dbkey_parser.set_defaults(func=dbkey)

    return parser


def main():

    parser = get_parser()
    args = parser.parse_args()

    if args.subparser_name:
        response = args.func(args)
        if response:
            print(response)
    else:
        parser.print_help()


if __name__ == '__main__':

    main()
