from settings.base import *  # noqa

# ----------------------------------------------
#
DEBUG = False
WSGI_APPLICATION = 'deploy.prod.wsgi.application'
ASGI_APPLICATION = 'deploy.prod.asgi.application'

# ----------------------------------------------
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
ALLOWED_HOSTS = []
INTERNAL_IPS = []

# ----------------------------------------------
# Channels configuration
#
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
