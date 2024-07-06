# DEALERSYNC/dealer_sync_backend/dealer_sync_backend/__init__.py
from .celery import app as celery_app

__all__ = ('celery_app',)