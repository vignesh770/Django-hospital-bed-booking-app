from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import bookpatient.routing

application = ProtocolTypeRouter ({
    'websocket': AuthMiddlewareStack(
        URLRouter (
            bookpatient.routing.websocket_urlpatterns
        )
    )
})


