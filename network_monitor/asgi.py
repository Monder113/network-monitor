# network_monitor/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import switch.routing # switch uygulamamızın routing dosyasını import edeceğiz (bir sonraki adımda oluşturulacak)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_monitor.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            switch.routing.websocket_urlpatterns
        )
    ),
})