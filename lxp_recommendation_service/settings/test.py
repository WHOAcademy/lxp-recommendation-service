from .base import *


# cache is mocked during unit tests, so an external cache is not defined here

NOSE_ARGS = [
    '--cover-erase',
    '--cover-package=recommendation_app',
    '--with-xunit',
    '--xunit-file=xunittest.xml',
    '--cover-branches',
]

LXP_COURSE_SERVICE = 'http://test-lxp-course-service.labs-test:8080'
LXP_PROFILE_SERVICE = 'http://test-lxp-profile-service.labs-test:3000'
