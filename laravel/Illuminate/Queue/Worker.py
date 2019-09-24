from gevent import monkey

import time

import gevent

import asyncio



class Worker():
    def __init__(self, app):
        self.queue = 'default'
        self.app = app
        self.redis = app.make('redis')
        self.callQueueHandler = app.make('callQueueHandler')
        self._loop = asyncio.get_event_loop()

    def onQueue(self, queue):
        self.queue = queue
        return self

    # gevent 实现流程
    #
    # def run(self):
    #     monkey.patch_all()
    #     # pool = Pool(500)
    #     while True:
    #         # 注意jobs是一个json字符串组成的列表
    #         jobs = self.redis.zrangebyscore('queue:' + self.queue + ':delayed', 0, int(time.time()),
    #                                               withscores=False)
    #
    #         for job in jobs:
    #             gevent.spawn(self.runJob, job)
    #         # 协程池map方法会造成主线程阻塞|当前需要是主线程不阻塞
    #         # pool.map(self.coroutine, jobs)
    #
    #         # 以下方式会阻塞主线程|当前需要是主线程不阻塞
    #         # gevent.joinall([gevent.spawn(self.runJob, job) for job in jobs])
    #
    #         # 适当睡眠避免cup空转
    #         time.sleep(1)
    #
    # def runJob(self, job):
    #     # 每次进入移除当前任务
    #     self.redis.zrem('queue:' + self.queue + ':delayed', job)
    #     self.callQueueHandler.call(job)

    # asyncio 实现流程
    def run(self):

        self._loop.create_task(self.start())

        self._loop.run_forever()


    # 开启服务
    async def start(self):
        while True:
            # 注意jobs是一个json字符串组成的列表
            jobs = self.redis.zrangebyscore('queue:' + self.queue + ':delayed', 0, int(time.time()),
                                                  withscores=False)

            for job in jobs:
                self._loop.create_task(self.runJob(job))

            # 适当睡眠避免cup空转
            await asyncio.sleep(1)


    # 消费
    async def runJob(self,job):
        self.redis.zrem('queue:' + self.queue + ':delayed', job)
        await self.callQueueHandler.call(job)
