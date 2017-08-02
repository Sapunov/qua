import os
import datetime


PROGRAM_NAME = 'qua'

APP_NAME = PROGRAM_NAME + '.ext'

VAR = '/var'

VAR_LIB = os.path.join(VAR, 'lib')

VAR_LOG = os.path.join(VAR, 'log')

LOGS_DIR = os.path.join(VAR_LOG, PROGRAM_NAME)

DATA_DIR = os.path.join(VAR_LIB, PROGRAM_NAME, 'data')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'somestrongdjangokey'

DEBUG = True

ALLOWED_HOSTS = ['*']

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

INSTALLED_APPS = [
    'api.apps.ApiConfig',
    'retriever.apps.RetrieverConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'app.middleware.LoggingMiddleware',
]

APPEND_SLASH = False

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': APP_NAME.replace('.', '_'),
        'HOST': '127.0.0.1' if DEBUG else 'postgresserver',
        'PORT': 5432,
        'USER': 'quauser',
        'PASSWORD': 'somestrongdbpassword'
    }
}

REDIS = {
    'host': '127.0.0.1' if DEBUG else 'redisserver',
    'port': 6379,
    'db_cache': 0,
    'db_persistent': 1
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{0}:{1}/{2}'.format(
            REDIS['host'],
            REDIS['port'],
            REDIS['db_cache']),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': APP_NAME
    }
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
    'EXCEPTION_HANDLER': 'app.exceptions.api_exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'app.response.jwt_response_payload_handler',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(DATA_DIR, 'static')

PAGE_SIZE = 10

MAIN_SEARCH_SERVICE_NAME = 'qua_main'

MAIN_SEARCH_SERP_LOCATION = 'middle'

SERP_MIDDLE_BLOCK_SIZE = PAGE_SIZE

SERP_TOP_BLOCK_SIZE = 1

SERP_RIGHT_BLOCK_SIZE = 3

# If we use docker environment and inside container application runs on port 80
# than there we must specify port 80 because of container interconnection
SERVICES = {
    'search': {
        MAIN_SEARCH_SERVICE_NAME: {
            'host': 'http://qua-search'
        }
    }
}
