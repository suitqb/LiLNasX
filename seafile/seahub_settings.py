# -*- coding: utf-8 -*-
import os

SECRET_KEY = os.environ['SEAHUB_SECRET_KEY']
SERVICE_URL = "https://cloud.balezeau.fr"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'seahub_db',
        'USER': 'seafile',
        'PASSWORD': os.environ['SEAHUB_DB_PASSWORD'],
        'HOST': 'mariadb',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': 'memcached:11211',
    },
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
COMPRESS_CACHE_BACKEND = 'locmem'
TIME_ZONE = 'Europe/Paris'
FILE_SERVER_ROOT = "https://cloud.balezeau.fr/seafhttp"

CSRF_TRUSTED_ORIGINS = ['https://cloud.balezeau.fr']

ENABLE_OAUTH = True
OAUTH_ENABLE_INSECURE_TRANSPORT = False

OAUTH_CREATE_UNKNOWN_USER = True
OAUTH_ACTIVATE_USER_AFTER_CREATION = True

OAUTH_CLIENT_ID = 'gFIdpvfP7tGn3sU4P8GNjzLLnkLjybNrbsLkhtlC'
OAUTH_CLIENT_SECRET = os.environ['OAUTH_CLIENT_SECRET']

OAUTH_REDIRECT_URL = 'https://cloud.balezeau.fr/oauth/callback/'

OAUTH_PROVIDER = 'authentik'
OAUTH_PROVIDER_DOMAIN = 'https://authentik.balezeau.fr'
OAUTH_AUTHORIZATION_URL = 'https://authentik.balezeau.fr/application/o/authorize/'
OAUTH_TOKEN_URL         = 'https://authentik.balezeau.fr/application/o/token/'
OAUTH_USER_INFO_URL     = 'https://authentik.balezeau.fr/application/o/userinfo/'

OAUTH_SCOPE = ["openid", "profile", "email"]

OAUTH_ATTRIBUTE_MAP = {
    "email": (True, "contact_email"),
    "name":  (False, "name"),
    "sub":   (False, "uid"),
}

LOGIN_URL = 'https://cloud.balezeau.fr/oauth/login/'
CLIENT_SSO_VIA_LOCAL_BROWSER = True
