from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_SERVICE_HOST'),
        'PORT': os.getenv('DATABASE_SERVICE_PORT'),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{SERVICE_HOST}:{SERVICE_PORT}/1".format(SERVICE_HOST=os.getenv('REDIS_SERVICE_HOST'),
                                                                     SERVICE_PORT=os.getenv('REDIS_SERVICE_PORT')),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.getenv('REDIS_PASSWORD')
        }
    }
}
