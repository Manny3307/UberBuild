from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from cleaningrecord_views import consumers

ws_patterns = [
    path('appmsg/', consumers.AppMessages.as_asgi())
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(ws_patterns))
})