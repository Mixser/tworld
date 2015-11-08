from .base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True
CURRENT_HOST = '127.0.0.1'
BASE_URL = 'http://' + CURRENT_HOST

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'mikeit.me <noreply@mikeit.me>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

ADMINS = (
    ('Dev Email', 'admin@mail.com'),
)

PROJECT_REQUEST_ADMINS = MANAGERS = ADMINS

CELERY_ALWAYS_EAGER = True
