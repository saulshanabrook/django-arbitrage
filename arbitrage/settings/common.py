from os import path

from django.conf.global_settings import *

import arbitrage

SITE_ROOT = path.dirname(path.realpath(arbitrage.__file__))

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
#Django
########
DEBUG = False

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
  )

STATIC_URL = '/static/'
STATIC_ROOT = path.normpath(path.join(SITE_ROOT, '../static/'))


#Admin
LOGIN_URL = '/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

#Urls
ROOT_URLCONF = 'arbitrage.urls'

