from .base import *             # NOQA
import sys


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True


# Define STATIC_ROOT for the collectstatic command

#STATIC_ROOT = join(BASE_DIR,  'static')

# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384
if "celery" in sys.argv[0]:
    DEBUG = False

# Django Debug Toolbar
INSTALLED_APPS += (
    'debug_toolbar.apps.DebugToolbarConfig',)

# Show emails to console in DEBUG mode
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Show thumbnail generation errors
THUMBNAIL_DEBUG = True




