from inspect import isgenerator, isasyncgen
from bald_spider.exceptions import TransformTypeError


async def transform(func_result):
    if isgenerator(func_result):  # 判断是否是一个生成器
        for r in func_result:
            yield r
    elif isasyncgen(func_result):  # 判断是否是一个异步的生成器
        async for r in func_result:   # 异步生成器 需要异步循环
            yield r
    else:
        raise TransformTypeError('callback return must be `generator` or `async generator``')
