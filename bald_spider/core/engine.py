import asyncio
from inspect import iscoroutine

from bald_spider import Request
from bald_spider.core.downloader import Downloader
from typing import Optional, Generator, Callable    # 导入更多的类型注解 使代码更严谨  Optional[其他类型] = None (可选择的，
# 可以是其他类型或者None)  Generator 生成器类型
from bald_spider.core.scheduler import Scheduler
from bald_spider.spider import Spider
from bald_spider.utils.spider import transform
from bald_spider.exceptions import OutputError
from bald_spider.task_manager import TaskManager
# engine负责把整个架构串联起来


class Engine:
    def __init__(self):
        self.spider: Optional[Spider] = None              # 初始化 爬虫实例       Optional: 可选类型，表示一个值可以为指定类型或None
        self.downloader: Optional[Downloader] = None      # 初始化 下载器
        self.scheduler: Optional[Scheduler] = None        # 初始化 调度器  调度器用于把请求入队出队
        self.start_requests: Optional[Generator] = None   # 初始化 起始请求
        self.task_manager: TaskManager = TaskManager()    # 初始化 task_manager  用来管理协程任务
        self.running = False

    async def start_spider(self, spider):  # spider 是传递过来的爬虫实例
        self.running = True
        self.spider = spider
        self.scheduler = Scheduler()
        if hasattr(self.scheduler, 'open'):
            self.scheduler.open()
        self.downloader = Downloader()

        # 这里使用iter 的作用是防止 在写爬虫程序的时候 自己创建了start_requests方法没有用yield而是用的return  iter的功能是把可迭代对象创建成迭代器对象
        self.start_requests = iter(spider.start_requests())
        # 获取到迭代器对象后开始走组逻辑
        await self._open_spider()

    async def _open_spider(self):

        crawling = asyncio.create_task(self.crawl())  # 创建任务   任务 被用来设置日程以便 并发 执行协程。
        await crawling           # await 后面的都是可等待对象   协程通过 async/await 语法进行声明

    async def crawl(self):
        """主逻辑"""
        while self.running:
            request = await self._get_next_request()
            if request is not None:
                await self._crawl(request)
            else:
                try:
                    start_requests = next(self.start_requests)    # noqa
                except StopIteration:
                    self.start_requests = None
                except Exception as exc:
                    # 1. 等请求的task 运行完毕
                    # 2.调度器是否空闲  也就是 优先级队列是否 为空
                    # 3. 下载器是否空闲
                    if not await self._exit():
                        continue
                    self.running = False
                else:
                    # 入队
                    await self.enqueue_request(start_requests)

    async def _crawl(self, request):
        # todo 实现并发
        async def crawl_task():
            outputs = await self._fetch(request)
            # 处理outputs
            if outputs:
                await self._handle_spider_output(outputs)

        # asyncio.create_task(crawl_task(), name='crawl')   # 创建协程任务  # 3.7版本的python 没有传name的属性
        # asyncio.create_task(crawl_task())   # 创建协程任务
        await self.task_manager.semaphore.acquire()  # 任务减1   限制并发数 ，当并发数达到上限 这里会阻塞
        self.task_manager.create_task(crawl_task())

    async def _fetch(self, request):
        async def _success(_response):  # 请求成功的情况下
            callback: Callable = request.callback or self.spider.parse   # 获取回调 注解：Callable 注解表示 可调用对象类型，用于表示函数类
            _outputs = callback(_response)
            if _outputs:     # 判断 _outputs 是否有值
                if iscoroutine(_outputs):  # 判断_outputs 是否是一个协程函数
                    await _outputs
                else:
                    return transform(_outputs)

        _response = await self.downloader.fetch(request)
        outputs = await _success(_response)
        return outputs

    async def enqueue_request(self, requests):
        await self._schedule_request(requests)

    async def _schedule_request(self, requests):
        # todo 去重
        await self.scheduler.enqueue_request(requests)

    async def _get_next_request(self):  # 出队
        return await self.scheduler.next_request()

    async def _handle_spider_output(self, outputs):
        async for spider_output in outputs:
            # print(spider_output)
            if isinstance(spider_output, Request):  # 判断output是否是请求 是的话入队
                await self.enqueue_request(spider_output)

            # elif:   # 判断 output是否是数据  暂时不处理 数据暂定 Item
            else:  # 以上都不是，直接抛出异常

                raise OutputError(f"{type(self.spider)} must return 'Request' or 'Item'")

    async def _exit(self):
        if self.scheduler.idle() and self.downloader.idle() and self.task_manager.all_done():  # 当都没有空闲都不退出
            return True

        return False  # 条件都空闲 就退出
