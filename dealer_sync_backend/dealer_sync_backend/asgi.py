"""
ASGI config for dealer_sync_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from scraper import routing as scraper_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealer_sync_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            scraper_routing.websocket_urlpatterns
        )
    ),
})
