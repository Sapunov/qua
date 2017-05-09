import os
import datetime

from qua import settings as qua_settings


APP_NAME = qua_settings.PROGRAM_NAME + '.api'

SECRET_KEY = 'somestrongdjangokey'

DEBUG = True

ALLOWED_HOSTS = ['*']

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

INSTALLED_APPS = [
    'api.apps.ApiConfig',
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
    'qua.rest.middleware.LoggingMiddleware',
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

if DEBUG:
    DATABASE_HOST = '127.0.0.1'
    REDIS_HOST = '127.0.0.1'
else:
    DATABASE_HOST = qua_settings.POSTGRESQL['host']
    REDIS_HOST = qua_settings.REDIS['host']

DATABASES = {
    'default': {
        'ENGINE': qua_settings.POSTGRESQL['engine'],
        'NAME': APP_NAME.replace('.', '_'),
        'HOST': DATABASE_HOST,
        'PORT': qua_settings.POSTGRESQL['port'],
        'USER': qua_settings.POSTGRESQL['user'],
        'PASSWORD': qua_settings.POSTGRESQL['password']
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{0}:{1}/{2}'.format(
            REDIS_HOST,
            qua_settings.REDIS['port'],
            qua_settings.REDIS['db_cache']
        ),
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
    'EXCEPTION_HANDLER': 'qua.rest.exceptions.api_exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'qua.rest.response.jwt_response_payload_handler',
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
            'filename': os.path.join(qua_settings.LOGS_DIR, APP_NAME + '.log'),
            'formatter': 'verbose'
        },
        'requests': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(
                qua_settings.LOGS_DIR, APP_NAME + '.requests.log'),
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

STATIC_ROOT = os.path.join(qua_settings.DATA_DIR, 'static')
