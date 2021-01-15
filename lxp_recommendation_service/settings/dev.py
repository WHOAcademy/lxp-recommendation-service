from .base import *

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

LXP_COURSE_SERVICE = 'http://test-lxp-course-service.labs-test:8080'
LXP_PROFILE_SERVICE = 'http://test-lxp-profile-service.labs-test:3000'
