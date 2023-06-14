from msgspec import Struct, msgpack, json
import json as _json
import orjson
from models import Request

js = None
with open("test.json", "rb") as f:
    js = f.read()


# 计算函数运行时间
def caculate_time(func):
    import time

    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(end - start)

    return inner


request = Request(url="https://www.baidu.com/content-search.xml", callback="parse")
d = {"url": "https://www.baidu.com/content-search.xml", "callback": "parse"}
print(request)


@caculate_time
def test0():
    for i in range(1000):
        json.decode(js)

@caculate_time
def test1():
    for i in range(1000):
        orjson.loads(js)

@caculate_time
def test2():
    for i in range(1000):
        _json.loads(js)


test0()
