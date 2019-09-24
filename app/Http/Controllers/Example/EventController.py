from app.Http.Controllers.Controller import Controller
from laravel.Helps.Help import app, jsonResponse, viewResponse
from app.Events.UserRegister import UserRegister
from random import randint
import asyncio


class EventController(Controller):
    async def index(self, request):
        # 定义监听（事件类及监听类方式）
        # app('events').listen('app.Events.UserRegister', 'app.Listeners.UserRegisterListener')

        # 定义监听 (闭包形式）
        # app('events').listen('test',self.userRegister())

        # 一组事件公用一个监听
        # app('events').listen(['foo', 'bar', 'baz'], 'app.Listeners.UserRegisterListener')

        # 一个事件被多个监听者监听可以在app/Providers/EventServiceProvider下定义

        # 建议在app/Providers/EventServiceProvider定义监听

        # 事件类继承Dispatchable可以用如下方式调用
        # await UserRegister.dispatch({'name': 'admin'})
        # 方式二
        # await app('events').dispatch(UserRegister({'name': 'admin'}))
        # 方式三
        # await app('events').dispatch('app.Events.UserRegister', {'name': 'admin'})

        # 框架提供的方法
        # 返回一个所有任务完成的futrue 和一个tasks列表
        # future, tasks = await app('events').dispatch(UserRegister({'name': 'admin'}),returnExceptions=True)
        # [task.add_done_callback(self.getSingleCallback()) for task in tasks]
        # future.add_done_callback(self.getAllDoneCallback('一组完成'))

        # task写法 （原生写法一，通过任务的形式、推荐）
        # tasks = [asyncio.create_task(self.task()) for _ in range(10)]
        #
        # for task in tasks:
        #     task.add_done_callback(self.getSingleCallback())
        #
        # future = asyncio.gather(*tasks)
        #
        # future.add_done_callback(self.getAllDoneCallback('all task done'))

        # coro写法 （原生写法二）
        # coros = [self.task() for _ in range(10)]
        #
        # future = asyncio.gather(*coros)
        #
        # future.add_done_callback(self.getAllDoneCallback('all done'))
        #

        # 延迟任务
        # loop = asyncio.get_running_loop()
        #
        # result = loop.call_later(5,self.test(),'this is a test',5)

        # 用多线程的方式解决无法找到适配的异步客户端
        from concurrent.futures import ThreadPoolExecutor
        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor()
        loop.run_in_executor(executor, self.ioBlocking)
        # tasks = [loop.run_in_executor(executor,self.ioBlocking) for _ in range(10)]
        # [task.add_done_callback(self.getIoBlockingCallback()) for task in tasks]
        return viewResponse('task has done')

    def ioBlocking(self):
        import time
        time.sleep(3)
        print('task is done')

    def getIoBlockingCallback(self):
        def ioBlockingCallback(self):
            print('ioBlockingCallback')
        return ioBlockingCallback

    async def task(self):
        from random import randint
        sec = randint(1, 4)
        await asyncio.sleep(sec)
        print('in task {}'.format(sec))
        return sec

    def getSingleCallback(self):
        def callback(future):
            print('single {} finished'.format(future.result()))

        return callback

    def getAllDoneCallback(self, word):
        def callback(future):
            print(word)
            print('all results {}'.format(future.result()))

        return callback

    def test(self):
        def closure(word,t):
            print(word,t)
            return '11111'
        return closure

    def userRegister(self):
        async def closure(payload):
            sec = randint(1, 5)
            await asyncio.sleep(sec)
            print(payload, 'called with closure', sec)
            return sec

        return closure