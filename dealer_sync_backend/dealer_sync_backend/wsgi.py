"""
WSGI config for dealer_sync_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
import os
import warnings
warnings.warn(
    "WSGI is deprecated for this project. Use ASGI instead.", DeprecationWarning)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dealer_sync_backend.settings")

application = get_wsgi_application()
