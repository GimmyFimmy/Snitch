import enum, asyncio, threading

from flask import *
from nextcord import *
from nextcord.ext.commands import *

TOKENS_AND_IDS = {
    "BOT_TOKEN": None,
    "CHANNEL_ID": None
}

WEBHOOK_DATA_SAMPLE = {
    "push": {
        "username": "{data[pusher][name]}",
        "info": {
            "Commit Message": "{data[head_commit][message]}\n",
            "`Forced": "{data[forced]}`"
        }
    },
    "pull_request": {
        "username": "{data[sender][name]}",
        "info": {
            "Action": "{data[action]}\n",
            "`Number": "{data[number]}`",
        }
    },
    "release": {
        "username": "{data[release][author][name]}",
        "info": {
            "Name": "{data[release][name]}",
            "Action": "{data[action]}\n",
            "`Pre Release": "{data[release][prerelease]}`",
            "`Id": "{data[release][id]}`",
        }
    },
    "issues": {
        "username": "{data[sender][login]}",
        "info": {
            "Name": "{data[issue][title]}",
            "Author": "{data[issue][user][login]}\n",
            "`Id": "{data[issue][id]}`",
        }
    }
}

WEBHOOK_MESSAGE_SAMPLE = {
    "title": "New {header} from {username}",
    "desc": "{key}: {value}\n"
}

class ResponseType(enum.Enum):
    Ok = ["Ok", 200]
    Invalid = ["Invalid", 400]
    AccessDenied = ["Access Denied", 403]
    UnexpectedError = ["Unexpected Error", 500]

class ResponseResult:
    def __new__(cls, response_type: ResponseType, response="") -> Response:
        assert type(response_type) == ResponseType
        assert type(response) == str

        return Response(response={response_type.value[0]: response}, status=response_type.value[1])

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
        assert (type(title) == str)
        assert (type(desc) == str)

        return Embed(
            title=title,
            description=desc,
            color=Color.dark_purple()
        )

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
        try:
            sample = WEBHOOK_DATA_SAMPLE.get(header)
            return Convert.__write_data(sample=sample, data=data)
        finally:
            pass

    @staticmethod
    def data_to_embed(header: str, data: dict) -> Embed:
        title_sample = WEBHOOK_MESSAGE_SAMPLE.get('title')
        desc_sample = WEBHOOK_MESSAGE_SAMPLE.get('desc')

        try:
            username = data.get('username')
            info = data.get('info')

            title = str.format(title_sample, header=header, username=username)
            desc = ''.join(desc_sample.format(key=key, value=value) for key, value in info.items())

            return Message(title=title, desc=desc)
        finally:
            pass

class Client:
    def __init__(self):
        self.intents = Intents.all()
        self.client = Bot(command_prefix="/", intents=self.intents)

    def run(self) -> ():
        try:
            token = TOKENS_AND_IDS.get("BOT_TOKEN")

            if token:
                return self.client.run(token)
        finally:
            pass

    def get_channel(self) -> Thread:
        try:
            if self.client.is_ready():
                channel_id = TOKENS_AND_IDS.get("CHANNEL_ID")

                if channel_id:
                    return self.client.get_channel(channel_id)
        finally:
            pass

    def send(self, header: str, data: dict) -> ():
        try:
            if self.client.is_ready():
                target_channel = self.get_channel()

                json_to_data = Convert.json_to_data(header=header, data=data)
                data_to_embed = Convert.data_to_embed(header=header, data=json_to_data)

                return asyncio.run_coroutine_threadsafe(target_channel.send(embed=data_to_embed), self.client.loop)
        finally:
            pass

try:
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

    def start():
        client_thread = threading.Thread(target=client.run, daemon=True)
        client_thread.start()

        server.run(port=3000)

    def set_key_or_token(key: str, value: any):
        for __key in TOKENS_AND_IDS.keys():
            if __key == key:
                TOKENS_AND_IDS[__key] = value
finally:
    pass