import html
import json
import logging
from datetime import datetime

import websockets
from asyncio import gather

from .commons import AbstractResponse, Message, BotMessage, AttackCommand, Sound, UserList


class Scorbot:

    MIN_RESPONSE_INTERVAL = 2 # in seconds

    def __init__(self, cookie: str, channel: str, domain: str, port: int, method: str):

        # setting up variables required by the server. The default is a Kabutops on the main lou server, I think
        self.cookie = cookie
        self.channel = "" if channel == "root" else channel
        self.domain = domain
        self.port = port
        self.method = method
        self.user_list = None # type: UserList
        self.ui_events_coro = list()

    def register_ui_event(self, coro):
        self.ui_events_coro.append(coro)

    async def _send_message(self, message):
        logging.debug("Sending message to server")
        if isinstance(message, dict):
            await self.socket.send(json.dumps(message))
        elif isinstance(message, bytes):
            await self.socket.send(message)

    async def _dispatch_response(self, response_obj : AbstractResponse):
        if isinstance(response_obj, (Message, BotMessage, AttackCommand)):
            await self._send_message(response_obj.to_dict())
        elif isinstance(response_obj, Sound):
            await self._send_message(response_obj.get_bytes())

    async def _on_connect(self, msg_data):
        # registering the user to the user list
        self.user_list.add_user(msg_data["userid"], msg_data["params"])
        logging.info("%s connected" % self.user_list.name(msg_data["userid"]))

    async def _on_disconnect(self, msg_data):
        # removing the user from the userlist
        logging.info("%s disconnected" % self.user_list.name(msg_data["userid"]))
        self.user_list.del_user(msg_data["userid"])

    async def socket_listener(self):
        while True:
            msg = await self.socket.recv()
            if type(msg) != bytes:
                msg_data = json.loads(msg, encoding="utf-8")
                msg_type = msg_data.get("type", "")
                if msg_type == "userlist":
                    self.user_list = UserList(msg_data["users"])
                    logging.info(str(self.user_list))

                elif msg_type == "connect":
                    await self._on_connect(msg_data)

                elif msg_type == "disconnect":
                    await self._on_disconnect(msg_data)

            else:
                logging.debug("Received sound file")

    async def ui_event_msg(self, ui_coro):
        msg = await ui_coro()
        await self._send_message(msg)

    async def listen(self):
        if self.method == "https":
            socket_address = 'wss://%s/socket/%s' % (self.domain, self.channel)
        else:
            socket_address = 'ws://%s:%i/socket/%s' % (self.domain, self.port, self.channel)
        logging.info("Listening to socket on %s" % socket_address)
        async with websockets.connect(socket_address,
                                      extra_headers={"cookie": "id=%s" % self.cookie}) as websocket:
            self.socket = websocket
            ui_coro_producers = [self.ui_event_msg(coro) for coro in self.ui_events_coro]
            await gather(self.socket_listener(), *ui_coro_producers)


