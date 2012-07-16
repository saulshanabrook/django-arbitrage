import os

from django.conf.global_settings import *


DIRNAME = os.path.dirname(__file__)

########
#Arbitrage
########

INSTALLED_APPS = (

  )


########
#External Packages
########
INSTALLED_APPS += (
    'south',
    'grappelli',
  )

GRAPPELLI_ADMIN_TITLE = 'arbitrage'


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
  )

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DIRNAME, '../static/')


#Admin
LOGIN_URL = '/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

#Urls
ROOT_URLCONF = 'arbitrage.urls'

