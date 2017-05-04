import os


PROGRAM_NAME = 'qua'

APP_NAME = ''

VAR = '/var'

VAR_LIB = os.path.join(VAR, 'lib')

VAR_LOG = os.path.join(VAR, 'log')

LOGS_DIR = os.path.join(VAR_LOG, PROGRAM_NAME)

DATA_DIR = os.path.join(VAR_LIB, PROGRAM_NAME, 'data')

ELASTICSEARCH = {
    'hosts': 'esserver',
    'timeout': 30,
    'max_retries': 10,
    'retry_on_timeout': True
}

REDIS = {
    'host': 'redisserver',
    'port': 6379,
    'db_cache': 0,
    'db_persistent': 1
}

POSTGRESQL = {
    'host': 'postgresserver',
    'port': '5432',
    'user': 'quauser',
    'password': 'somestrongdbpassword',
    'engine': 'django.db.backends.postgresql_psycopg2'
}

MAX_SEARCH_RESULTS = 100
