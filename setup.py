from setuptools import setup, find_packages

setup(name='lxp-recommendation-service',
      version='1.1.0',
      packages=find_packages(),
      install_requires=[
          'Django~=3.0.8',
          'psycopg2-binary~=2.8.5',
          'djangorestframework~=3.11.0',
          'nose==1.3.7',
          'coverage==5.2.1',
          'django-nose==1.4.6',
          'drf-yasg==1.17.1',
          'django-cors-headers==3.4.0',
          'django-redis==4.12.1',
          'requests==2.24.0'
      ],
      scripts=['manage.py'])