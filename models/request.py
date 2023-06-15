from typing import Any
from msgspec import Struct


class Request(Struct, omit_defaults=True):
    url: str
    callback: str = None
    method: str = "GET"
    params: dict = None
    headers: dict = None
    cookies: dict = None
    json: Any = None
    data: bytes | str = None
    verify_ssl: bool = False
    meta: dict = None
    errback: str = None
    req_kwargs: dict = {}


if __name__ == "__main__":
    request = Request(url="https://www.baidu.com/content-search.xml", callback="parse")
    print(request.__struct_config__)
