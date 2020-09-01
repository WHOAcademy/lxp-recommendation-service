import os 

def get_service_url(service_name):
    """Return service url based on its name."""

    if service_name == 'COURSE_SERVICE':

        if 'LXP_COURSE_SERVICE' in os.environ:
            
            return os.getenv('LXP_COURSE_SERVICE')

        else:

            return 'https://test-lxp-course-service-labs-test.apps.who.emea-2.rht-labs.com'

    else:

        return ''
