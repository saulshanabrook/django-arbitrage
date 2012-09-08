from memcacheify import memcacheify
import dj_database_url

from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

########
#Cache
########

CACHES = memcacheify()  # http://rdegges.github.com/django-heroku-memcacheify/
MIDDLEWARE_CLASSES = ('django.middleware.gzip.GZipMiddleware',) + MIDDLEWARE_CLASSES

########
#Database
########
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

########
#Server
########
INSTALLED_APPS += ('gunicorn',)
INTERNAL_IPS = ('0.0.0.0',)
