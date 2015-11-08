import os

ENV = os.environ.get('ENV', 'DEV').upper()

DEV = 'DEV' == ENV
STAGING = 'STAGING' == ENV
PROD = 'PROD' == ENV

if DEV:
    from .dev import *
elif STAGING:
    pass
elif PROD:
    pass