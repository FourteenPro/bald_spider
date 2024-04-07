from asyncio import PriorityQueue, TimeoutError  # priorityQueue 是优先级队列
import asyncio


class SpiderPriorityQueue(PriorityQueue):
    def __init__(self, maxsize=0):
        super(SpiderPriorityQueue, self).__init__(maxsize=maxsize)  #

    async def get(self):  # 重写了PriorityQueue的get方法
        f = super().get()  # 调用父级的get方法
        try:
            return await asyncio.wait_for(f, timeout=0.1)
        except TimeoutError:
            return None
