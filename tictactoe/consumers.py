from channels.generic.websocket import AsyncWebsocketConsumer
import json
from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv("DEVELOPMENT"):
    redis = Redis(host='localhost', port=6379, db=0)
else:
    redis = Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=int(os.getenv("REDIS_DB")), password=os.getenv("REDIS_PASS"))

class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "lobby_group",
            self.channel_name,
        )
        await self.accept()
        if self.scope["path"] == "/ws/lobby":
            user = self.scope["user"]
            message = user.username
            host = self.scope["query_string"].decode("utf-8")[2:]
            if not redis.hgetall(f"lobby:{message}") and host == message:
                redis.hmset(f"lobby:{message}", {"players_count": 1, "opponent": ""})
                await self.channel_layer.group_send(
                    "lobby_group", {"type": "created_lobby", "message": message}
                )
            elif (
                redis.hgetall(f"lobby:{host}")
                and int(redis.hget(f"lobby:{host}", "players_count")) == 1
                and host != message
            ):
                redis.hmset(f"lobby:{host}", {"players_count": 2, "opponent": message})
                await self.channel_layer.group_send(
                    "lobby_group",
                    {"type": "new_player", "message": f"{host},{message}"}
                )

        await self.send(
            text_data=json.dumps(
                {"type": "connection_established", "message": "Connected"}
            )
        )

    async def disconnect(self, close_code):
        user = self.scope["user"]
        message = user.username
        host = self.scope["query_string"].decode("utf-8")[2:]
        if redis.hgetall(f"lobby:{message}"):
            redis.delete(f"lobby:{message}")
            await self.channel_layer.group_send(
                "lobby_group", {"type": "deleted_lobby", "message": f"{host},{message}"}
            )
        else:
            if host and redis.hgetall(f"lobby:{host}"):
                redis.hmset(f"lobby:{host}", {"players_count": 1, "opponent": ""})
                await self.channel_layer.group_send(
                    "lobby_group",
                    {"type": "player_leave", "message": f"{host},{message}"}
                )
        await self.channel_layer.group_discard("lobby_group", self.channel_name)
        await self.send(
            text_data=json.dumps(
                {"type": "connection_closed", "message": "Disconnected"}
            )
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data.get("type")
        message = data.get("message")

        if type == "lobby":
            if redis.hgetall(f"lobby:{message}"):
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "players_count",
                            "message": int(
                                redis.hget(f"lobby:{message}", "players_count")
                            ),
                        }
                    )
                )
        if type == "start_match":
            await self.channel_layer.group_send(
                "lobby_group", {"type": "started_match", "message": message}
            )

    async def created_lobby(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps({"type": "created_lobby", "message": message})
        )

    async def deleted_lobby(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps({"type": "deleted_lobby", "message": message})
        )

    async def new_player(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps({"type": "new_player", "message": message})
        )

    async def player_leave(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps({"type": "player_leave", "message": message})
        )

    async def started_match(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps({"type": "started_match", "message": message})
        )


class MatchConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        host = self.scope["query_string"].decode("utf-8")[2:].split(",")[0]
        opponent = self.scope["query_string"].decode("utf-8")[2:].split(",")[1]
        await self.channel_layer.group_add(f"match_{host}_group", self.channel_name)
        await self.accept()
        redis.hmset(f"match:{host}", {"opponent": opponent})
        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "message": f"Connected to {host} vs {opponent} match"
                }
            )
        )

    async def disconnect(self, close_code):
        host = self.scope["query_string"].decode("utf-8")[2:].split(",")[0]
        await self.channel_layer.group_send(
            f"match_{host}_group",
            {"type": "connection_closed", "message": "Disconnected"}
        )

        await self.channel_layer.group_discard(f"match_{host}_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data.get("type")
        message = data.get("message")
        host = self.scope["query_string"].decode("utf-8")[2:].split(",")[0]

        if type == "new_move":
            await self.channel_layer.group_send(
                f"match_{host}_group",
                {
                    "type": "move",
                    "message": {"move": message["move"], "player": message["player"]},
                }
            )

        if type == "reset_match":
           await self.channel_layer.group_send(
                f"match_{host}_group",
                {
                    "type": "reset",
                    "message": {"player": message["player"]}
                }
            ) 

    async def move(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"type": "move", "message": message}))

    async def reset(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"type": "reset", "message": message}))

    async def connection_closed(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"type": "connection_closed", "message": message}))
