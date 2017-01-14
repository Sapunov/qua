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

STATIC_ROOT = os.path.join(DATA, 'static')

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
            'NAME': os.path.join(DATA, 'database.sqlite3'),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE":   "django.db.backends.postgresql_psycopg2",
            "NAME":     "qua",
            "USER":     "qua_user",
            "PASSWORD": "18pic81j67j4wDz",
            "HOST":     "localhost",
            "PORT":     "5432",
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
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',)
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'qua.api.response.custom_jwt_response_payload_handler',
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(filename)s:"
                      "%(funcName)s:%(lineno)s "
                      "%(levelname)s: %(message)s"
        },
        "simple": {
            "format": "%(asctime)s %(message)s"
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
        "requests": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGS_DIR, "requests.log"),
            "formatter": "simple"
        },
    },
    "loggers": {
        "qua": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True
        },
        "qua.requests": {
            "handlers": ['requests'],
            "level": "INFO",
            "propagate": False
        }
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