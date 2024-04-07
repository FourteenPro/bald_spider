from bald_spider import Request
from bald_spider.spider import Spider


class BaiduSpider(Spider):  # 继承 Spider 自己有方法用自己的 自己没有父类有用父类的
    start_urls = ['https://www.baidu.com', 'https://www.baidu.com']
    # start_url = 'https://www.baidu.com'

    async def parse(self, response):   # 解析响应中  有可能生成 新的url 和 数据  防止在这里有i/o操作 把协程的情况兼容进来
        print('parse:', response)
        for i in range(10):     # 模拟生成新的 url
            url = 'https://www.baidu.com'
            request = Request(url=url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        print('parse_page：result')
        for i in range(10):     # 模拟生成新的 url
            url = 'https://www.baidu.com'
            request = Request(url=url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        print('parse_detail：result')






