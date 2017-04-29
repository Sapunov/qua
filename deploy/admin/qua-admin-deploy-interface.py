#!/usr/bin/python3

import argparse
import errno
import os
import re
import shutil
import sys


BASE_PATH = os.path.join('/var', 'www', 'qua')
INDEX_PATH = os.path.join(BASE_PATH, 'index.html')
STATIC_PATH = os.path.join(BASE_PATH, 'static')
BACKUP_DIR = os.path.join(BASE_PATH, '.backup')


def create_dir(dirpath):

    try:
        os.mkdir(dirpath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e


def delete_files(directory):

    for the_file in os.listdir(directory):
        file_path = os.path.join(directory, the_file)

        if os.path.isfile(file_path):
            os.unlink(file_path)


def replace_static_paths(filename):

    with open(filename, 'r+') as opened:
        html = opened.read()

        html = re.sub(r'(href|src)="([a-z]{2,})', r'\1="/static/\2', html)
        html = re.sub(r'<title>(\w)+</title>', r'<title>QUA</title>', html)

        opened.seek(0)
        opened.write(html)
        opened.truncate()

    print('Staticfiles paths replaces. File saved in: {0}'.format(filename))


def copy_index(filename):

    shutil.copyfile(filename, INDEX_PATH)

    print('Index file copied to: {0}'.format(INDEX_PATH))


def copy_staticfiles(directory):

    delete_files(STATIC_PATH)

    for the_file in os.listdir(directory):
        if the_file == 'index.html':
            continue

        file_path = os.path.join(directory, the_file)

        if os.path.isfile(file_path):
            shutil.copy(file_path, os.path.join(STATIC_PATH, the_file))

    print('Staticfiles copied to: {0}'.format(STATIC_PATH))


def backup():

    backup_dir_static = os.path.join(BACKUP_DIR, 'static')

    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)

    create_dir(BACKUP_DIR)
    create_dir(backup_dir_static)

    if os.path.exists(INDEX_PATH):
        shutil.copy(INDEX_PATH, os.path.join(BACKUP_DIR, 'index.html'))
        print('{0} backuped'.format(INDEX_PATH))

    if os.path.exists(STATIC_PATH):
        count = 0

        for the_file in os.listdir(STATIC_PATH):
            file_path = os.path.join(STATIC_PATH, the_file)

            if os.path.isfile(file_path):
                shutil.copy(file_path, backup_dir_static)
                count += 1

        print('{0} static files backuped'.format(count))


def check_directories():

    for directory in (BASE_PATH, STATIC_PATH):
        if not os.path.exists(directory):
            print('{0} does not exist'.format(directory))
            sys.exit(1)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--dist', help='Dist directory', required=True)

    args = parser.parse_args()

    check_directories()
    backup()

    dist_directory = os.path.abspath(args.dist)

    index_html = os.path.join(dist_directory, 'index.html')

    replace_static_paths(index_html)

    copy_index(index_html)
    copy_staticfiles(dist_directory)


if __name__ == '__main__':
    main()
