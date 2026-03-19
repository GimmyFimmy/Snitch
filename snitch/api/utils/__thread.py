"""
    Desc: Util to run method(s) asynchronously
    Creator: Kirosha
"""

from threading import Thread, ThreadError
from asyncio import run_coroutine_threadsafe, AbstractEventLoop, Future

from typing import Coroutine

from snitch.api.utils.__logger import log_err

def run_thread(target: callable) -> Thread | None:
    try:
        thread = Thread(target=target, daemon=True)
        thread.start()
        return thread
    except ThreadError as err:
        return log_err(err)

def run_coroutine(coro: Coroutine, loop: AbstractEventLoop) -> Future | None:
    try:
        coroutine = run_coroutine_threadsafe(coro=coro, loop=loop)
        return coroutine
    except Exception as err:
        return log_err(err)