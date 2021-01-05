"""
ASGI config for GoldDigger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.core.urls import url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoldDigger.settings')

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from GDapp.consumers import AnalysisConsumer

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,
    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^run_gd/$", AnalysisConsumer.as_asgi()),
        ])
    ),
})