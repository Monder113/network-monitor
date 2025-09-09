from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/switch_updates/$', consumers.SwitchStatusConsumer.as_asgi()),
    path('ws/switch/<int:switch_id>/cli/', consumers.SwitchCliConsumer.as_asgi()),
]