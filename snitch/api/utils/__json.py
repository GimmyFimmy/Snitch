"""
    Desc: Util to read .json file(s) and response to event(s)
    Creator: Kirosha
"""
from flask import jsonify
from json import load, JSONDecodeError
from os.path import abspath, dirname, join, normpath

from snitch.api.utils.__logger import log_err

# returns a correct path to snitch/config directory
CONFIG_DIRECTORY = normpath(join(dirname(abspath(__file__)), "..", "..", "config"))

def read(name: str) -> dict | list | None:
    try:
        file_path = join(CONFIG_DIRECTORY, f"{name}.json")
        with open(file_path, "r", encoding="utf-8") as file:
            return load(file)
    except (JSONDecodeError, FileNotFoundError) as err:
        return log_err(err)

def response(message: str, http_status: any) -> tuple:
    return jsonify("OK" if message == "OK" else {"error": message}), http_status.value