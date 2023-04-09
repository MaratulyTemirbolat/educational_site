from settings.base import *  # noqa

# ----------------------------------------------
#
DEBUG = True
WSGI_APPLICATION = None
ASGI_APLLICATION = None

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
