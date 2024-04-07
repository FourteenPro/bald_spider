from bald_spider.core.engine import Engine
from tests.baidu_spider.baidu import BaiduSpider
import asyncio
import time
from bald_spider.utils.project import get_settings


async def run():
    # 代码规范 srp  单一职责原则  single responsibility principle
    settings = get_settings()
    baidu_spider = BaiduSpider()
    engine = Engine()
    await engine.start_spider(baidu_spider)

s = time.time()
asyncio.run(run())   # asyncio.run() 函数用来运行最高层级的入口

print(time.time()-s)
