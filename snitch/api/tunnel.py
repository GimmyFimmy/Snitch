"""
    Desc: Tunnel class to create tunnel between server and GitHub
    Creator: Kirosha
"""

from subprocess import call

from snitch.api.utils.__logger import *
from snitch.api.utils.__thread import run_thread
from snitch.api.utils.__requests import send_redirect

class Tunnel:
    def __init__(self):
        self.url = send_redirect("https://smee.io/new")

    def run(self) -> None:
        if self.url:
            log_ok(f"Connected to the tunnel with link: {self.url}")

            def target():
                call(args="npm install --global smee-client", shell=True)
                call(args=f"smee -u {self.url}", shell=True)

            run_thread(target=target)
        else:
            log_err("Failed to connect to tunnel")

    def get_url(self) -> str | None:
        return self.url