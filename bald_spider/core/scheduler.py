# 调度器   把请求调度到请求队列中
# 队列选择有序队列
from typing import Optional
from bald_spider.utils.pqueue import SpiderPriorityQueue


class Scheduler:
    def __init__(self):
        self.requests_queue: Optional[SpiderPriorityQueue] = None

    def open(self):  # 初始化队列
        self.requests_queue = SpiderPriorityQueue()

    async def next_request(self):   # 获取下一个请求  请求出队
        request = await self.requests_queue.get()
        return request

    async def enqueue_request(self, requests):  # 请求入队
        # await asyncio.sleep(1)
        await self.requests_queue.put(requests)

    def idle(self) -> bool:  # -> bool 表示方法返回布尔值
        return len(self) == 0   # 单队列返回0 代表队列是空闲状态

    def __len__(self):  # 当对对象进行len操作时 对象会调用 __len__ 方法
        return self.requests_queue.qsize()
