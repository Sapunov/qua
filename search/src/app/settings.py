import os


PROGRAM_NAME = 'qua'

APP_NAME = PROGRAM_NAME + '.search'

VAR = '/var'

VAR_LIB = os.path.join(VAR, 'lib')

VAR_LOG = os.path.join(VAR, 'log')

LOGS_DIR = os.path.join(VAR_LOG, PROGRAM_NAME)

DATA_DIR = os.path.join(VAR_LIB, PROGRAM_NAME, 'data')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'somestrongdjangokey'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'rest_framework',
    'search.apps.SearchConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.LoggingMiddleware'
]

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(filename)s:'
                      '%(funcName)s:%(lineno)s '
                      '%(levelname)s: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(message)s'
        },
    },
    'handlers': {
        'qua': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, APP_NAME + '.log'),
            'formatter': 'verbose'
        },
        'requests': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, APP_NAME + '.requests.log'),
            'formatter': 'simple'
        }
    },
    'loggers': {
        'qua': {
            'handlers': ['qua'],
            'level': 'DEBUG',
            'propagate': True
        },
        'qua.requests': {
            'handlers': ['requests'],
            'level': 'INFO',
            'propagate': False
        }
    },
}

ELASTICSEARCH = {
    'hosts': ['127.0.0.1' if DEBUG else 'esserver'],
    'timeout': 30,
    'max_retries': 10,
    'retry_on_timeout': True
}

ES_DOCTYPE = 'main'

ES_SEARCH_INDEX = PROGRAM_NAME + '_search'

ES_SPELLING_INDEX = PROGRAM_NAME + '_spelling'

ES_SEARCH_FIELDS = ('title^4', 'keywords^2', 'text')

DEFAULT_PAGE_SIZE = 10

MAIN_SEARCH_SERVICE_NAME = 'qua_main'

MAIN_SEARCH_SERP_LOCATION = 'middle'
