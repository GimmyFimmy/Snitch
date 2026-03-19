"""
    Desc: Util to send get/post/delete request(s)
    Creator: Kirosha
"""

from requests import get, post, delete, exceptions

from snitch.api.utils.__logger import log_err

# delete status
OK_STATUS = [200, 201, 204]

def __safe_call(target: callable) -> str | dict | None:
    def wrapper(*args, **kwargs):
        try:
            return target(*args, **kwargs)
        except (exceptions.ConnectionError, exceptions.HTTPError, exceptions.Timeout) as err:
            log_err(err)
    return wrapper

@__safe_call
def send_redirect(url: str) -> str | None:
    response = get(url=url, allow_redirects=True)
    response.raise_for_status()
    return response.url

@__safe_call
def send_post(url: str, headers: dict, payload: dict) -> dict | None:
    response = post(url=url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

@__safe_call
def send_delete(url: str, headers: dict) -> None:
    response = delete(url=url, headers=headers)
    if response.status_code not in OK_STATUS:
        return log_err(f"Delete Error: {response.status_code}")