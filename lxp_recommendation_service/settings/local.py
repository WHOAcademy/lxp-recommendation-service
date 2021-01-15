from .base import *

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

LXP_COURSE_SERVICE = 'https://test-lxp-course-service-labs-test.apps.who.lxp.academy.who.int'
LXP_PROFILE_SERVICE = 'https://test-lxp-profile-service-labs-test.apps.who.lxp.academy.who.int'
