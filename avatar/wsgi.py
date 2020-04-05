"""
WSGI config for avatar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('/opt/bitnami/apps/django/django_projects/avatar')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/avatar/egg_cache")


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avatar.settings')

application = get_wsgi_application()