class Request:
    def __init__(self, url=None, callback=None, errback=None, form=None, headers=None, method="get", meta=None,
                 dont_filter=False, priority=None, *args, **kwargs):
        self.method: str = method
        self.url: str = url
        self.callback: callable = callback
        self.errback: callable = errback
        self.headers: dict = headers
        self.form: dict = form
        self.meta: dict = meta or {}
        self.dont_filter: bool = dont_filter
        # 优先级，越小越先请求
        self.priority: int = -(priority or 0)

        # 创建body，供指纹使用
        if method.lower() == "get":
            self.body = url.split("?", 1)[-1].encode() if "?" in url else b""
        elif method.lower() == "post":
            self.body = "&".join(map(lambda _: "=".join(_), sorted(form.items(), key=lambda x: x[0]))).encode()

    # 供优先级队列比较，比较的是Request.priority的大小

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __str__(self):
        return f"<{self.method.upper()} {self.url}>"


class FormRequest(Request):
    def __init__(self, url=None, callback=None, errback=None, form=None, headers=None, meta=None,
                 dont_filter=False, *args, **kwargs):
        self.method = "post"
        super(FormRequest, self).__init__(url, callback, errback, form, headers, self.method, meta, dont_filter, *args, **kwargs)
