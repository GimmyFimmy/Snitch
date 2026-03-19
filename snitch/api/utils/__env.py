"""
    Desc: Util to access .env file(s)
    Creator: Kirosha
"""

from os import getenv
from dotenv import load_dotenv
from os.path import abspath, dirname, join, normpath

# returns a correct path to snitch/config/tokens.env file
ENV_PATH = normpath(join(dirname(abspath(__file__)), "..", "..", "config", "tokens.env"))

load_dotenv(dotenv_path=ENV_PATH)

def get_token(name: str) -> str:
    return getenv(f"{name}_TOKEN")