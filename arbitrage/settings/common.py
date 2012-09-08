from os import path, environ

import arbitrage

SITE_ROOT = path.dirname(path.realpath(arbitrage.__file__))

########
#Default
########
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

########
#Arbitrage
########
INSTALLED_APPS = (
    'arbitrage.apps.stocks',
)

########
#External Packages
########
INSTALLED_APPS += (
    'south',
    'grappelli',
  )

GRAPPELLI_ADMIN_TITLE = 'Arbitrage'

########
#Django Boilerplate
########
INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
  )

SECRET_KEY = environ.get('SECRET_KEY', '*YSHFUIH&GAHJBJCZKCY)P#R')

STATIC_URL = '/static/'
STATIC_ROOT = path.normpath(path.join(SITE_ROOT, '../static/'))

FIXTURE_DIRS = (path.join(SITE_ROOT, 'fixtures'),)

LOGIN_URL = '/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

ROOT_URLCONF = 'arbitrage.urls'
