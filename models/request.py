

class Request:
    def __init__(
        self,
        url,
        callback=None,
        *,
        method="GET",
        params=None,
        headers=None,
        cookies=None,
        json=None,
        data=None,
        verify_ssl=False,
        meta=None,
        cb_kwargs=None,
        **kwargs,
    ):
        self.__req_args__ = {
            "url": url,
            "method": method,
            "params": params,
            "headers": headers,
            "cookies": cookies,
            "json": json,
            "data": data,
            "verify_ssl": verify_ssl,
            **kwargs,
        }
        self.callback = callback
        self.meta = meta
        self.cb_kwargs = cb_kwargs

    def __repr__(self):
        return f"<Request {self.__req_args__['method']} {self.__req_args__['url']}>"

    def serialize(self):
        return self.__dict__

    @classmethod
    def build_from_dict(self, request_dict):
        return Request(**request_dict)


if __name__ == "__main__":
    request = Request.build_from_dict({"url": "https://www.baidu.com/content-search.xml", "callback": "parse"})
    print(request.serialize())
