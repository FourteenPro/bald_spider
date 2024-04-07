from typing import Optional, Dict, Callable


class Request:
    def __init__(
        self, url: str, *,                     # * 号后面的参数 是必须的关键字参数
        headers: Optional[Dict] = None,        # 请求头
        callback: Optional[Callable] = None,   # 回调函数， 用于把请求结果回调回来
        priority: int = 0,                     # 权重
        method: str = 'GET',                   # 请求方式
        cookies: Optional[Dict] = None,        # cookie
        proxy: Optional[Dict] = None,          # 代理
        body='',                               # body
    ):
        self.url = url
        self.headers = headers
        self.callback = callback
        self.priority = priority
        self.method = method
        self.cookies = cookies
        self.proxy = proxy
        self.body = body

    def __lt__(self, other):  # 当要比较两个对象大小时 会调用这个方法  优先级队列里会用到  这个方法是放小于大于的
        return self.priority < other.priority
