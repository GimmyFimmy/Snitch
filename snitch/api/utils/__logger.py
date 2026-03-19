"""
    Desc: Util to print log(s)
    Creator: Kirosha
"""

# green color
OK_FORMAT = "\033[92m\033[1m{msg}\033[0m"
# red color
ERR_FORMAT = "\033[91m\033[1m{msg}\033[0m"

def __print(msg: str, formatting: str) -> None:
    log = formatting.format(msg=f"[SNITCH]: {msg}")
    print(log)

def log_err(msg: str) -> None:
    return __print(msg, ERR_FORMAT)

def log_ok(msg: str) -> None:
    return __print(msg, OK_FORMAT)