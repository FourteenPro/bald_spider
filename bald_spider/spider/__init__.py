from bald_spider import Request


# 创建爬虫的基类
class Spider:
    def __init__(self):
        if not hasattr(self, 'start_urls'):  # 判断对象中是否有这个属性
            self.start_urls = []

    def start_requests(self):
        if self.start_urls:     # 判断列表是否有元素
            for url in self.start_urls:
                yield Request(url=url)
        else:
            # 判断对象中是否有start_url属性 且 属性是否是字符串
            if hasattr(self, 'start_url') and isinstance(getattr(self, 'start_url'), str):
                yield Request(url=getattr(self, 'start_url'))

    def parse(self, response):
        raise NotImplementedError    # 抛出异常
