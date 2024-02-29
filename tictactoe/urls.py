from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ranking", views.ranking, name="ranking"),
    path("logout", views.logout_view, name="logout"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("playing_options", views.playing_options, name="playing_options"),
    path("lobby_list", views.lobby_list, name="lobby_list"),
    path("lobby/<str:player_one>", views.lobby, name="lobby"),
    path("match_room", views.match_room, name="match_room"),
    path("match", views.match, name="match"),
    path("ranking", views.ranking, name="ranking"),
    path("error", views.error, name="error")
]