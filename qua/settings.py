import os
import datetime

ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC = os.path.join(ROOT, "static")
DATA = os.path.join(ROOT, "data")
LOGS_DIR = os.path.join(ROOT, "logs")

SECRET_KEY = '7dz6*-2e%4mi1gsh)9ko9)0ocv@cb8z_cfjuez0(^8aa3+1+d-'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

STATICFILES_DIRS = (
    STATIC,
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

INSTALLED_APPS = [
    'qua.api',
    'qua.wi',
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
]

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA, 'database.sqlite3'),
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
    'EXCEPTION_HANDLER': 'qua.api.exceptions.custom_api_exception_handler',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=14)
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s FN:%(filename)s M:%(module)s "
                      "FU:%(funcName)s L:%(lineno)s "
                      "%(levelname)s:%(message)s"
        },
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGS_DIR, "django.log"),
            "formatter": "verbose"
        },
    },
    "loggers": {
        "qua": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(DATA, 'cache'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
