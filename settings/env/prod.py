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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dtalpu6hl0c5j',
        'USER': 'ovfcpsfpknvmxc',
        'PASSWORD': '0dc04a3857bd803bb3d7d11480c3f6bf360daee45a21a9f21ba75c255ce29adf',  # noqa
        'HOST': 'ec2-44-195-132-31.compute-1.amazonaws.com',
        'PORT': 5432
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
