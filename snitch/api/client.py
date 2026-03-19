"""
    Desc: Client class to send message(s) via Discord bot
    Creator: Kirosha
"""

from typing import Optional

from nextcord import Intents, Color, Embed
from nextcord.abc import GuildChannel
from nextcord.ext.commands import Bot

from snitch.api.utils.__json import *
from snitch.api.utils.__logger import *
from snitch.api.utils.__thread import *

__samples = read("events")

# message(s) color configuration
color = __samples.get("color", {})
r = color.get("r", 255)
g = color.get("g", 255)
b = color.get("b", 255)

def embed(title: str, desc: str) -> Embed:
    return Embed(
        title=title,
        description=desc,
        color=Color.from_rgb(r=r, g=g, b=b)
    )

def extract_data(header: str, payload: dict) -> list | None:
    try:
        sample = __samples.get(header)
        if not sample: return log_err(f"No sample for {header}")

        title_sample = sample.get("title")
        desc_sample = sample.get("desc")
        channel_id = sample.get("channel_id")

        if not all([title_sample, desc_sample, channel_id]): return log_err(f"Incomplete sample for {header}")

        title = title_sample.format(data=payload)
        desc = desc_sample.format(data=payload)

        return [embed(title=title, desc=desc), channel_id]
    except Exception as err:
        return log_err(f"Error while extracting data: {err}")

class Client:
    def __get_channel(self, channel_id: int) -> Optional[GuildChannel]:
        if not self.client.is_ready(): return log_err("Bot is not ready")
        try:
            return self.client.get_channel(channel_id)
        except Exception as err:
            return log_err(f"Error while getting channel: {err}")


    def __init__(self, token: str):
        self.intents = Intents.all()
        self.client = Bot(command_prefix="/", intents=self.intents)

        self._token = token

        @self.client.event
        async def on_ready():
            log_ok(f"Initialized Discord bot with token: {self._token}")

        @self.client.event
        async def on_error(event, *args, **kwargs):
            log_err(f"Error in event {event}: {args} {kwargs}")

    def run(self) -> None:
        try:
            run_thread(lambda: self.client.run(self._token))
        except Exception as err:
            return log_err(f"Error while initializing Discord bot: {err}")

    def send(self, header: str, payload: dict) -> None:
        if not self.client.is_ready(): return log_err("Bot is not ready")
        try:
            data = extract_data(header, payload)
            if not data: return

            channel = self.__get_channel(int(data[1]))
            if not channel: return log_err(f"Missing channel with id: {data[1]}")

            run_coroutine(channel.send(embed=data[0]), self.client.loop)
        except Exception as err:
            return log_err(f"Error while sending message: {err}")
        else:
            log_ok("Successfully sent message")