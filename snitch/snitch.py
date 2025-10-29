from subprocess import call

from threading import Thread
from asyncio import run_coroutine_threadsafe

from requests import get
from http import HTTPStatus
from flask import request, Flask, jsonify

from nextcord import Intents, Embed, Color
from nextcord.ext.commands import Bot

_CACHE = {}

_SAMPLES = {
    "push": {
        "title": "↗ Push from {data[pusher][name]}",
        "desc": "`Commit Messages:`\n{data[head_commit][message]}\n\n`Forced: {data[forced]}`",
    },
    "pull_request": {
        "title": "⤵ {data[pull_request][title]} was *{data[action]}* by {data[sender][login]}",
        "desc": "`Number: {data[number]}`",
    },
    "release": {
        "title": "⬇ {data[release][name]} was *{data[action]}* by {data[release][author][login]}",
        "desc": "`Pre Release: {data[release][prerelease]}`\n`Id: {data[release][id]}`",
    },
    "issues": {
        "title": "⚠ {data[issue][title]} was *{data[action]}* by {data[issue][user][login]}",
        "desc": "`Id: {data[issue][id]}`",
    },
}


class _Task:
    def __new__(cls, target: callable) -> Thread:
        assert callable(target)

        thread = Thread(target=target, daemon=True)
        thread.start()
        return thread


class _Request:
    @staticmethod
    def redirected_url(url: str) -> str:
        response = get(url, allow_redirects=True)

        if response.status_code == 200:
            url = response.url
            return url


class _Receive:
    @staticmethod
    def method() -> str:
        return request.method

    @staticmethod
    def header() -> str:
        return request.headers.get("X-Github-Event")

    @staticmethod
    def json() -> dict:
        return request.get_json()


class _Message:
    def __new__(cls, title: str, desc: str) -> Embed:
        assert type(title) == str
        assert type(desc) == str

        return Embed(title=title, description=desc, color=Color.from_rgb(85, 0, 255))


class _Convert:
    def __new__(cls, header: str, data: dict) -> Embed:
        header_samples = _SAMPLES.get(header)

        title_sample = header_samples.get("title")
        desc_sample = header_samples.get("desc")

        title = str.format(title_sample, data=data)
        desc = str.format(desc_sample, data=data)

        return _Message(title=title, desc=desc)


class _Client:
    def __init__(self):
        self.intents = Intents.all()
        self.client = Bot(command_prefix="/", intents=self.intents)

    def run(self) -> ():
        token = _CACHE.get("BOT_TOKEN")

        return self.client.run(token)

    def get_channel(self, header: str):
        header = str.upper(header)

        if self.client.is_ready():
            channel_id = _CACHE.get(f"{header}_CHANNEL_ID")

            if channel_id:
                channel_id = int(channel_id)

                return self.client.get_channel(channel_id)

    def send(self, header: str, data: dict) -> ():
        if self.client.is_ready():
            target_channel = self.get_channel(header=header)
            target_embed = _Convert(header=header, data=data)

            if target_channel and target_embed:
                return run_coroutine_threadsafe(
                    target_channel.send(embed=target_embed), self.client.loop
                )
            else:
                print("[-] No target channel or embed message")


client = _Client()
server = Flask(__name__)


class Snitch:
    @staticmethod
    def __connect_to_server() -> ():
        try:
            server.run(port=3000)
        except Exception as Result:
            print(f"[!] {Result}")

    @staticmethod
    def __connect_to_client() -> ():
        try:
            _Task(target=client.run)
        except Exception as Result:
            print(f"[!] {Result}")

    @staticmethod
    def __connect_to_tunnel() -> ():
        try:
            url = _Request.redirected_url("https://smee.io/new")

            def target():
                call("npm install --global smee-client", shell=True)
                call(f"smee -u {url}", shell=True)

            _Task(target=target)
        except Exception as Result:
            print(f"[!] {Result}")

    @staticmethod
    @server.route(rule="/", methods=["POST"])
    def __webhook():
        method = _Receive.method()

        if method != "POST":
            return (
                jsonify({"error": "POST method only allowed"}),
                HTTPStatus.METHOD_NOT_ALLOWED.value,
            )

        try:
            data = _Receive.json()
            header = _Receive.header()

            if data and header and header in _SAMPLES:
                client.send(header=header, data=data)
                return jsonify("OK"), HTTPStatus.OK.value
            else:
                return (
                    jsonify({"error": "Wrong header or data"}),
                    HTTPStatus.BAD_REQUEST.value,
                )
        except Exception as Reason:
            return jsonify({"error": Reason}), HTTPStatus.INTERNAL_SERVER_ERROR.value

    @staticmethod
    def run(properties: dict) -> ():
        for key, value in properties.items():
            _CACHE[key] = value

        Snitch.__connect_to_tunnel()
        Snitch.__connect_to_client()
        Snitch.__connect_to_server()
