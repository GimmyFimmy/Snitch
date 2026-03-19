"""
    Desc: Webhook class to manage repository webhook
    Creator: Kirosha
"""

from copy import deepcopy
from atexit import register

from snitch.api.utils.__logger import *
from snitch.api.utils.__json import read
from snitch.api.utils.__requests import send_post, send_delete

class Webhook:
    def __get_url(self) -> str:
        return self.webhooks["url"]

    def __format_headers(self, section: str) -> dict:
        return {
            key: value.format(github_token=self.token)
            for key, value in self.webhooks[section]["headers"].items()
        }

    def __format_payload(self) -> dict:
        payload = deepcopy(self.webhooks["add"]["payload"])
        payload["config"]["url"] = self.url
        return payload

    def __add_webhook(self) -> None:
        url = self.__get_url()
        payload = self.__format_payload()
        headers = self.__format_headers("add")

        result = send_post(
            url=url,
            headers=headers,
            payload=payload
        )

        if result:
            self.id = result.get("id")
            log_ok(f"Created GitHub webhook with id: {self.id}")

    def __delete_webhook(self) -> None:
        url = f"{self.__get_url()}/{self.id}"
        headers = self.__format_headers("remove")

        send_delete(
            url=url,
            headers=headers
        )

    def __init__(self, token: str, payload_url: str):
        self.webhooks = read("webhooks")

        self.token = token
        self.url = payload_url

        self.id = None

    def run(self) -> None:
        self.__add_webhook()

        if self.id:
            register(self.__delete_webhook)
        else:
            log_err("Failed to create GitHub webhook")