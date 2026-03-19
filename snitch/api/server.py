"""
    Desc: Server class to handle GitHub request(s)
    Creator: Kirosha
"""

from flask import request, Flask
from http import HTTPStatus

from snitch.api.utils.__logger import *
from snitch.api.utils.__json import response

class Server:
    def __init__(self):
        self.__server = Flask(__name__)
        self.__handler = None

        @self.__server.route(rule="/", methods=["POST"])
        def webhook() -> tuple:
            if request.method != "POST":
                return response(message="POST method only allowed", http_status=HTTPStatus.METHOD_NOT_ALLOWED)
            try:
                payload = request.get_json()
                header = request.headers.get("X-Github-Event")
                if all([header, payload, self.__handler]):
                    self.__handler(
                        header=header,
                        payload=payload
                    )
                    return response(message="OK", http_status=HTTPStatus.OK)
                else:
                    return response(message="Wrong header or data", http_status=HTTPStatus.BAD_REQUEST)
            except Exception as err:
                log_err(f"Webhook route error: {err}")
                return response(message=str(err), http_status=HTTPStatus.BAD_REQUEST)

    def set_handler(self, predicate: callable) -> None:
        assert callable(predicate)
        self.__handler = predicate

    def run(self) -> None:
        log_ok("Connected to the Web-Server with port: 3000")
        self.__server.run(port=3000)