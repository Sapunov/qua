import os


PROGRAM_NAME = 'qua'

APP_NAME = PROGRAM_NAME

VAR = '/var'

VAR_LIB = os.path.join(VAR, 'lib')

VAR_LOG = os.path.join(VAR, 'log')

LOGS_DIR = os.path.join(VAR_LOG, PROGRAM_NAME)

DATA_DIR = os.path.join(VAR_LIB, PROGRAM_NAME, 'data')

ELASTICSEARCH = {
    'hosts': ['esserver'],
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

SERP_SIZE = 10

ES_DOCTYPE = 'main'

ES_SEARCH_INDEX = PROGRAM_NAME + '_search'

ES_SPELLING_INDEX = PROGRAM_NAME + '_spelling'

SEARCH_FIELDS = ['title^4', 'keywords^2', 'text']

# If one service doesn't respond within this timeout, qua trying to
# request another if exists
# By default - 1 sec
SERVICES_TIMEOUT = 1

MAIN_SEARCH_SERVICE_NAME = 'qua_main'

MAIN_SEARCH_SERP_LOCATION = 'middle'

SERP_MIDDLE_BLOCK_SIZE = SERP_SIZE

SERP_TOP_BLOCK_SIZE = 1

SERP_RIGHT_BLOCK_SIZE = 3
