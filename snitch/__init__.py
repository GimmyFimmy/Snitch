"""
    Desc: Snitch class to initialize other classes
    Creator: Kirosha
"""

from snitch.api.client import Client
from snitch.api.server import Server
from snitch.api.tunnel import Tunnel
from snitch.api.webhook import Webhook

from snitch.api.utils.__logger import log_err
from snitch.api.utils.__env import get_token

class Snitch:
    def __init__(self):
        self.__bot_token = get_token("BOT")
        self.__github_token = get_token("GITHUB")

        try:
            self.tunnel = Tunnel()
            self.tunnel.run()

            self.__payload_url = self.tunnel.get_url()
            if not self.__payload_url: return

            self.webhook = Webhook(
                token=self.__github_token,
                payload_url=self.__payload_url
            )
            self.webhook.run()

            self.client = Client(
                token=self.__bot_token
            )
            self.client.run()

            self.server = Server()
            self.server.set_handler(self.client.send)
            self.server.run()
        except Exception as err:
            log_err(f"Snitch failed to start: {err}")