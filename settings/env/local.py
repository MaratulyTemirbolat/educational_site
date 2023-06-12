from settings.base import *  # noqa

# ----------------------------------------------
#
DEBUG = True
WSGI_APPLICATION = None
ASGI_APPLICATION = 'deploy.test.asgi.application'

# ----------------------------------------------
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
INTERNAL_IPS = [
    "127.0.0.1",
]

# ----------------------------------------------
# Channels configuration
#
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    },
}
