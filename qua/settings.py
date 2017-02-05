import os
import datetime


PROGRAM_NAME = 'qua'

# /var/www/qua on production environment
ROOT = os.path.abspath(os.path.dirname(__file__))

VAR = '/var'
VAR_LIB = os.path.join(VAR, 'lib')
VAR_LOG = os.path.join(VAR, 'log')

LOGS_DIR = os.path.join(VAR_LOG, PROGRAM_NAME)
DATA_DIR = os.path.join(VAR_LIB, PROGRAM_NAME, 'data')

STATIC = os.path.join(ROOT, 'static')

SECRET_KEY = 'secret_key'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

STATICFILES_DIRS = (
    STATIC,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_ROOT = os.path.join(DATA_DIR, 'static')

INSTALLED_APPS = [
    'qua.api',
    'qua.ui',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'rest_framework',
    'corsheaders', # while development
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # while development
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware', # while development
    'django.contrib.messages.middleware.MessageMiddleware',
    'qua.api.middleware.LoggingMiddleware',
]

# While development
CORS_ORIGIN_WHITELIST = (
    'localhost:4200'
)

# While development
CORS_ALLOW_CREDENTIALS = True

APPEND_SLASH = False

ROOT_URLCONF = 'qua.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(ROOT, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'qua.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(DATA_DIR, 'database.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'qua',
            'USER':     'qua_user',
            'PASSWORD': 'password',
            'HOST':     'localhost',
            'PORT':     '5432',
        },
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'EXCEPTION_HANDLER': 'qua.api.exceptions.custom_api_exception_handler',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'qua.api.response.custom_jwt_response_payload_handler',
}

PAGE_SIZE = 10

REDIS_DB = 0

REDIS_URL = 'redis://localhost:6379/{}'.format(REDIS_DB)
BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_SEND_EVENTS = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


SEARCH_RESULTS_MAX = 100
SEARCH_INDEX_NAME = PROGRAM_NAME
SEARCH_INDEX_TYPE = 'questions'

CRAWLER = {
    'permitted_content_types': [
        'text/html',
        'application/pdf'
    ],
    'external_resources': {
        'jive.croc.ru': {
            'retriever': 'qua.api.search.extresources.JiveCrocRu',
            'auth': {
                'type': 'basic',
                'username': 'username',
                'password': 'password'
            }
        }
    }
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
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'qua': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'qua.log'),
            'formatter': 'verbose'
        },
        'requests': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'qua_api_requests.log'),
            'formatter': 'simple'
        },
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'celery.log'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 100,
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
        },
        'celery': {
            'handlers': ['celery'],
            'level': 'DEBUG',
            'propagate': True
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(DATA_DIR, 'cache'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
