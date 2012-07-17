import sys

from .common import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':  path.normpath(path.join(SITE_ROOT, '../sqlite.db')),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            }
    }

########
#Debug Toolbar
########
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)
INTERNAL_IPS = ('127.0.0.1')

########
#Testing
#######
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = path.normpath(path.join(SITE_ROOT, '..'))
TEST_DISCOVER_ROOT = path.join(TEST_DISCOVER_TOP_LEVEL, 'tests')
TEST_DISCOVER_PATTERN = '*.py'
if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
