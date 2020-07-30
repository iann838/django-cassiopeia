"""
Django settings for tests project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from datetime import timedelta as td

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_CASSIOPEIA_SECRET"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cassiopeia',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tests.urls'

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

WSGI_APPLICATION = 'tests.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Example django cache config
CACHES = {
    # Leave the "default" cache for handling data for your apps (preferable)
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/10", #db:10 for test
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },

    # Example cache for cass using "django-redis" (pip install)
    # For this backend you can define the pickle protocol version, default -1 (latest)
    # Check Out "django-redis" repository/docs for lot more flexible configurations.
    "cass-redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/11", #db:11 for test
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1
        }
    },
    # Example cache using FileBased backend that stores a max of 10k values
    'filebased': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'filebased-cache'),
        'MAX_ENTRIES': 10000,
    }
    # For more caching backends and/or configurations
    # Please check Django's cache framework documentation.
}

CASSIOPEIA_DEFAULT_REGION = "NA"
CASSIOPEIA_RIOT_API_KEY = os.environ["RIOT_API_KEY"]
CASSIOPEIA_LIMITING_SHARE = 1.0

CASSIOPEIA_LOGGING = {
    "PRINT_CALLS": True,
    # Do not set below value to True in production !!!
    "PRINT_RIOT_API_KEY": False,
    "DEFAULT": "WARNING",
    "CORE": "WARNING"
}
CASSIOPEIA_API_ERROR_HANDLING = {
    "404": ["t"],
    "500": ["^e", 3, 2, 3],
    "503": ["^e", 3, 2, 3],
    "TIMEOUT": ["^e", 3, 2, 3],
    "403": ["t"],
    "429": {
        "SERVICE": ["^e", 3, 2, 3],
        "METHOD": ["r", 5],
        "APPLICATION": ["r", 5],
    },
}
CASSIOPEIA_PIPELINE = {
    "Omnistone": {
        "EXPIRATIONS_MAP" : {
            td(hours=3): ["c", "c+", "r", "r+", "cr", "i", "i+", "pi", "pi+"],
            td(hours=6): ["rl", "v", "ss", "ss+", "mp", "mp+", "ls", "ls+"],
            0: ["*+"]
        },
        "MAX_ENTRIES": 6000,
        "CULL_FRECUENCY": 2,
        "SAFE_CHECK": True,
        "LOGS_ENABLED": False,
    },
    "DjangoCache": [
        {
            "ALIAS" : "cass-redis",
            "EXPIRATIONS_MAP" : {
                td(hours=6): ["rl-", "v-", "cr-", "cm-", "cm+-", "cl-", "gl-", "ml-"],
                td(days=7): ["mp-", "mp+-", "ls-", "ls+-", "t-", 'm-'],
                td(days=1): ["c-", "c+-", "r-", "r+-", "i-", "i+-", "ss-", "ss+-", "pi-", "pi+-", "p-"],
                td(minutes=15): ["cg-", "fg-", "shs-", "s-"],
                0: ["*-"]
            },
            "SAFE_CHECK": True,
            "LOGS_ENABLED": True,
        },
        {
            "ALIAS": "filebased",
            "EXPIRATIONS_MAP": {
                td(days=1): ["c-", "c+-", "r-", "r+-", "i-", "i+-", "ss-", "ss+-", "pi-", "pi+-", "p-"],
                0: ["*-"]
            },
            "SAFE_CHECK": True,
            "LOGS_ENABLED": True,
        }
    ],
    "DDragon": {},
    "RiotAPI": {},
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
