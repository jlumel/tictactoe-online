from django.urls import path
import tictactoe.consumers

websocket_urlpatterns = [
    path('ws/lobby', tictactoe.consumers.LobbyConsumer.as_asgi()),
    path('ws/lobby_list', tictactoe.consumers.LobbyConsumer.as_asgi()),
    path('ws/match', tictactoe.consumers.MatchConsumer.as_asgi())
]