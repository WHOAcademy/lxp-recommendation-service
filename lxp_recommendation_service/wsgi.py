"""
WSGI config for lxp_recommendation_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""


from django.core.wsgi import get_wsgi_application
from lxp_recommendation_service.preps import set_default_env

set_default_env()

application = get_wsgi_application()
