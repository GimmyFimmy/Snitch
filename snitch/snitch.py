"""
    CLASS SNITCH
        - Light Discord bot, which sends GitHub webhooks
        - Created by Gimmy_Fimmy
"""

"""
    LIBRARIES
"""

import enum, asyncio, threading, subprocess, requests

from flask import *
from nextcord import *
from nextcord.ext.commands import *

"""
    DICTIONARIES
        CACHE - dict for storing keys and ids
        WEBHOOK_DATA_SAMPLE - dict with data samples for every supported header
        WEBHOOK_MESSAGE_SAMPLE - dict with desc and title samples for embed message
"""

CACHE = {}

WEBHOOK_DATA_SAMPLE = {
    "push": {
        "username": "{data[pusher][name]}",
        "info": {"Commit Message": "{data[head_commit][message]}\n", "`Forced": "{data[forced]}`"},
    },
    "pull_request": {
        "username": "{data[sender][name]}",
        "info": {
            "Action": "{data[action]}\n",
            "`Number": "{data[number]}`",
        },
    },
    "release": {
        "username": "{data[release][author][name]}",
        "info": {
            "Name": "{data[release][name]}",
            "Action": "{data[action]}\n",
            "`Pre Release": "{data[release][prerelease]}`",
            "`Id": "{data[release][id]}`",
        },
    },
    "issues": {
        "username": "{data[sender][login]}",
        "info": {
            "Name": "{data[issue][title]}",
            "Author": "{data[issue][user][login]}\n",
            "`Id": "{data[issue][id]}`",
        },
    },
}

WEBHOOK_MESSAGE_SAMPLE = {"title": "New {header} from {username}", "desc": "{key}: {value}\n"}

"""
    CLASSES
        * _Task - threading class
        
        * ResponseType - response data converted into enum
        
        * CacheKeyType - cache keys converted into enum
        
        * ResponseResult - convert raw data into response
        
        * Request - request data from url
            > redirected_url - returns redirected url
            
        * Receive - receive data
            > method    - returns receive method (GET, POST)
            > header    - returns message header (push, pull_request, ping and etc)
            > json      - returns message itself
        
        * Message - create embed message from raw data
        
        * Convert - data convertion based on sample
            > __write_data      - writes input data values in a sample
            
            > json_to_data      - converts raw data in webhook data
            > data_to_embed     - converts webhook data in embed message
            
        * Client - class for controlling discord bot
            > run           - run bot (BOT_TOKEN required)
            > get_channel   - returns channel id based on header
            > send          - send message in a specific channel safely
"""


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

        return Embed(title=title, description=desc, color=Color.purple())


class Convert:
    @staticmethod
    def __write_data(sample: dict, data: dict) -> dict:
        result = {}

        for key, value in sample.items():
            if type(value) == str:
                result[key] = value.format(data=data)
            elif type(value) == dict:
                result[key] = Convert.__write_data(sample=value, data=data)
        return result

    @staticmethod
    def json_to_data(header: str, data: dict) -> dict:
        sample = WEBHOOK_DATA_SAMPLE.get(header)
        return Convert.__write_data(sample=sample, data=data)

    @staticmethod
    def data_to_embed(header: str, data: dict) -> Embed:
        title_sample = WEBHOOK_MESSAGE_SAMPLE.get("title")
        desc_sample = WEBHOOK_MESSAGE_SAMPLE.get("desc")

        username = data.get("username")
        info = data.get("info")

        title = str.format(title_sample, header=header, username=username)
        desc = "".join(desc_sample.format(key=key, value=value) for key, value in info.items())

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

            json_to_data = Convert.json_to_data(header=header, data=data)
            data_to_embed = Convert.data_to_embed(header=header, data=json_to_data)

            return asyncio.run_coroutine_threadsafe(
                target_channel.send(embed=data_to_embed), self.client.loop
            )


"""
    VARIABLES
        client  - initialize Client class
        server  - initialize Flask class
"""

client = Client()
server = Flask(__name__)

"""
    WRAPPED METHODS
        > webhook - receive webhooks and send messages
"""


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


"""
    PRIVATE METHODS
        > __connect_to_server   - startup Flask server
        > __connect_to_client   - startup Discord bot
        > __connect_to_tunnel   - startup Smee tunnel
"""


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


"""
    PUBLIC METHODS
        > run               - startup everything
        > set_key_value     - set key value in CACHE dict
"""


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
