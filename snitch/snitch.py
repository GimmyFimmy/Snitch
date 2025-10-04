import enum, asyncio, threading, subprocess, requests

from flask import *
from nextcord import *
from nextcord.ext.commands import *

CACHE = {}

SAMPLES = {
    "push": {
        "title": "↗ push from {data[pusher][name]}",
        "desc": "Commit Message: {data[head_commit][message]}\n\n`Forced: {data[forced]}`"
    },
    "pull_request": {
        "title": "⤵ pull request from {data[sender][name]}",
        "desc":"Action: {data[action]}\n\n`Number: {data[number]}`",
    },
    "release": {
        "title": "⬇ new release from {data[release][author][name]}",
        "desc": "Name: {data[release][name]}\nAction: {data[action]}\n\n`Pre Release: {data[release][prerelease]}`\n`Id: {data[release][id]}`",
    },
    "issues": {
        "username": "⚠ {data[sender][login]}",
        "desc": "Name: {data[issue][title]}\nAuthor: {data[issue][user][login]}\n\n`Id: {data[issue][id]}`"
    }
}

class _Task:
    def __new__(cls, target: callable) -> threading.Thread:
        assert callable(target)

        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        return thread


class ResponseType(enum.Enum):
    Ok = ["Ok", 200]
    Invalid = ["Invalid", 400]
    AccessDenied = ["Access Denied", 403]
    UnexpectedError = ["Unexpected Error", 500]

class CacheKeyType(enum.Enum):
    DiscordToken = "DISCORD_TOKEN"

    PushChannelId = "PUSH_CHANNEL_ID"
    PullRequestChannelId = "PULL_REQUEST_CHANNEL_ID"
    ReleaseChannelId = "RELEASE_CHANNEL_ID"
    IssuesChannelId = "ISSUES_CHANNEL_ID"

class ResponseResult:
    def __new__(cls, response_type: ResponseType, response="") -> Response:
        assert type(response_type) == ResponseType
        assert type(response) == str

        return Response(response={response_type.value[0]: response}, status=response_type.value[1])


class Request:
    @staticmethod
    def redirected_url(url: str) -> str:
        response = requests.get(url, allow_redirects=True)

        if response.status_code == ResponseType.Ok.value[1]:
            url = response.url
            return url


class Receive:
    @staticmethod
    def method() -> str:
        return request.method

    @staticmethod
    def header() -> str:
        return request.headers.get("X-Github-Event")

    @staticmethod
    def json() -> dict:
        return request.get_json()


class Message:
    def __new__(cls, title: str, desc: str) -> Embed:
        assert type(title) == str
        assert type(desc) == str

        return Embed(title=title, description=desc, color=Color.from_rgb(85, 0, 255))


class Convert:
    def __new__(cls, header: str, data: dict) -> Embed:
        header_samples = SAMPLES.get(header)

        title_sample = header_samples.get("title")
        desc_sample = header_samples.get("desc")

        title = str.format(title_sample, data=data)
        desc = str.format(desc_sample, data=data)

        return Message(title=title, desc=desc)

class Client:
    def __init__(self):
        self.intents = Intents.all()
        self.client = Bot(command_prefix="/", intents=self.intents)

    def run(self) -> ():
        token = CACHE.get(CacheKeyType.DiscordToken.value)

        return self.client.run(token)

    def get_channel(self, header: str) -> Thread:
        header = str.upper(header)

        if self.client.is_ready():
            channel_id = CACHE.get(f"{header}_CHANNEL_ID")

            if channel_id:
                channel_id = int(channel_id)

                return self.client.get_channel(channel_id)

    def send(self, header: str, data: dict) -> ():
        if self.client.is_ready():
            target_channel = self.get_channel(header=header)
            target_embed = Convert(header=header, data=data)

            return asyncio.run_coroutine_threadsafe(
                target_channel.send(embed=target_embed), self.client.loop
            )

client = Client()
server = Flask(__name__)

@server.route(rule="/", methods=["POST"])
def webhook():
    method = Receive.method()

    if method != "POST":
        return ResponseResult(response_type=ResponseType.AccessDenied)

    try:
        data = Receive.json()
        header = Receive.header()

        if data and header:
            client.send(header=header, data=data)
            return ResponseResult(response_type=ResponseType.Ok)
        else:
            return ResponseResult(response_type=ResponseType.Invalid)
    except Exception as Reason:
        return ResponseResult(response_type=ResponseType.UnexpectedError, response=str(Reason))
    finally:
        pass


def __connect_to_server() -> ():
    try:
        server.run(port=3000)
    except Exception as Result:
        raise Exception(Result)


def __connect_to_client() -> ():
    try:
        _Task(target=client.run)
    except Exception as Result:
        raise Exception(Result)


def __connect_to_tunnel() -> ():
    try:
        url = Request.redirected_url("https://smee.io/new")

        def target():
            subprocess.call("npm install --global smee-client", shell=True)
            subprocess.call(f"smee -u {url}", shell=True)

        _Task(target=target)
    except Exception as Result:
        raise Exception(Result)


def run() -> ():
    __connect_to_tunnel()
    __connect_to_client()
    __connect_to_server()


def set_key_value(key: CacheKeyType, value: any) -> ():
    try:
        assert type(key) == CacheKeyType

        CACHE[key.value] = value
    except Exception as Result:
        raise Exception(Result)