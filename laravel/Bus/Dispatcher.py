from laravel.Foundation.Bus.ShouldQueue import ShouldQueue
from laravel.Helps.Help import current_config


class Dispatcher():
    def __init__(self, app, queueResolver):
        self.app = app
        self.queueResolver = queueResolver

    async def dispatch(self, job):
        if isinstance(job, ShouldQueue):
            return self.dispatchToQueue(job)
        return await self.dispatchNow(job)

    async def dispatchNow(self, job):
        return await job.handle(job.payload)


    def dispatchToQueue(self, job):
        queue = self.__getQueueByDriver(job)

        return self.pushJobToQueue(queue, job)

    def __getQueueByDriver(self, job):
        return self.queueResolver(job.driver) \
            if hasattr(job, 'driver') \
            else self.queueResolver(current_config('queue.default'))

    def pushJobToQueue(self, queue, job):
        if hasattr(job, 'queue') and hasattr(job, 'delay'):
            return queue.laterOn(job.queue, job.delay, job)
        if hasattr(job, 'queue'):
            return queue.pushOn(job.queue, job)
        if hasattr(job, 'delay'):
            return queue.laterOn('default', job.delay, job)

        return queue.pushOn('default', job)
