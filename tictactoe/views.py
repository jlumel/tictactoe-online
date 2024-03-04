from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Player, Match
from redis import Redis
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv("DEVELOPMENT"):
    redis = Redis(host='localhost', port=6379, db=0)
else:
    redis = Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=int(os.getenv("REDIS_DB")), password=os.getenv("REDIS_PASS"))
redis.flushdb()

# Create your views here.

def index(request):
    return render(request, "tictactoe/index.html")

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"].lower()
        password = request.POST["password"]
        player = authenticate(request, username=username, password=password)

        if player is not None:
            login(request, player)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "tictactoe/login.html",
                {"message": "Invalid username and/or password"},
            )
    else:
        return render(request, "tictactoe/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "tictactoe/register.html", {"message": "Passwords must match"}
            )

        try:
            player = Player.objects.create_user(username, None, password)
            player.save()
        except IntegrityError:
            return render(
                request, "tictactoe/register.html", {"message": "Username already taken"}
            )
        login(request, player)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tictactoe/register.html")

@login_required
def ranking(request):
    return render(request, "tictactoe/ranking.html")

@login_required
def playing_options(request):
    return render(request, "tictactoe/playing_options.html")

@login_required
def lobby_list(request):
    lobby_keys = redis.keys('lobby*')
    filtered_lobby_keys = []
    if lobby_keys:
        for key in lobby_keys:
            value = int(redis.hget(key, "players_count"))
            if value == 1:
                filtered_lobby_keys.append(key)
        filtered_lobby_keys = [key.decode('utf-8') for key in filtered_lobby_keys]
        filtered_lobby_keys = [key[6:] for key in filtered_lobby_keys]     
    return render(request, "tictactoe/lobby_list.html", {"lobby_list": filtered_lobby_keys})

@login_required
def lobby(request, player_one):
    if redis.hgetall(f"lobby:{player_one}") and int(redis.hget(f"lobby:{player_one}", "players_count")) == 1:
        if request.user.username == player_one:
            return render(request, "tictactoe/lobby.html", {"player_one": player_one})
        else:
            player_two = request.user.username
            return render (request, "tictactoe/lobby.html", {"player_one": player_one, "player_two": player_two})
    elif redis.hgetall(f"lobby:{player_one}") and int(redis.hget(f"lobby:{player_one}", "players_count")) == 2:
        player_two = redis.hget(f"lobby:{player_one}", "opponent").decode('utf-8')
        return render (request, "tictactoe/lobby.html", {"player_one": player_one, "player_two": player_two})
    else:
        if player_one == request.user.username:
            return render(request, "tictactoe/lobby.html", {"player_one": player_one})
        else:
            return render(request, "tictactoe/error_page.html")

@login_required
def match_room(request):

    if request.method == "POST":
        player_one = request.POST["player_one"]
        player_two = request.POST["player_two"]

        return render(request, "tictactoe/match_room.html", {"player_one": player_one, "player_two": player_two})
    else:
        return render(request, "tictactoe/error_page.html")

@csrf_exempt
@login_required    
def match(request):
    if request.method == "POST":
        data = json.loads(request.body)
        player_one = Player.objects.get(username=data["player_one"])
        player_two = Player.objects.get(username=data["player_two"])
        if data["winner"]:
            is_draw = False
            winner = Player.objects.get(username=data["winner"])
            loser = Player.objects.get(username=data["loser"])
            match = Match(player_one=player_one, player_two=player_two, is_draw=is_draw, winner=winner, loser=loser)
        else:
            is_draw = True
            match = Match(player_one=player_one, player_two=player_two, is_draw=is_draw)
        match.save()
        return JsonResponse({"message": "Match created successfully"})
    elif request.method == "GET":
        player = Player.objects.get(username=request.user.username)
        matches = Match.objects.filter(Q(player_one=player) | Q(player_two=player))
        return render(request, "tictactoe/match_history.html", {"matches": matches})
        
@login_required    
def ranking(request):
    players = Player.objects.all()
    ranking = []
    for player in players:
        if player.username == "admin":
            continue
        match_history = player.get_match_statistics()
        ranking.append({"username": player.username, "match_history": match_history})
    ranking = sorted(ranking, key=lambda x: x["match_history"]["wins"], reverse=True)
    return render(request, "tictactoe/ranking.html", {"ranking": ranking})

def error(request):
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]
        path = request.POST["path"]
        return render(request, "tictactoe/error_page.html", {"title": title, "text": text, "path": path})
    else:
        return render(request, "tictactoe/error_page.html")