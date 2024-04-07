import asyncio
from typing import Set
from asyncio import Task, Future, Semaphore


class TaskManager:   # 管理 task（协程任务） 的类 也就是 并发数
    def __init__(self, total_concurrency=8):

        # self.current_task: Final[Set] = set()  # 3.7版本的 typing 没有 Final, Final 表示 变量设置了注解 这个量的类型只能是 set
        self.current_task: Set = set()
        self.semaphore: Semaphore = Semaphore(total_concurrency)

    def create_task(self, coroutine) -> Task:  # 方法返回 协程任务  传入一个协程 coroutine
        task = asyncio.create_task(coroutine)
        self.current_task.add(task)

        def done_callback(_fut: Future):   # 接受一个参数 类型是 future  给形参_fut加下划线告诉编译器 我用不上它 编辑器也不会警告 是一种编程规范
            # 这个函数为什么写在里面？  1. 可读性更强 2.因为done_callback只能接收一个参数 写在外面不好传参，偏要写在外面的话用 from functools import  partial(偏函数)
            self.current_task.remove(task)
            self.semaphore.release()        # 任务加1

        task.add_done_callback(done_callback)  # 添加一个回调，将在 Task 对象 完成 时被运行 调用 callback 时，Future 对象是它的唯一参数。

        return task

    def all_done(self):  # 判断任务数量是否为0 是就返回true
        return len(self.current_task) == 0

