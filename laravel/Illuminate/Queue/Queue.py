import time
import sync


class Queue(metaclass=sync.ABCMeta):
    def __init__(self, app):
        self.app = app

    @sync.abstractmethod
    def laterOn(self, queue, delay, job):
        pass

    @sync.abstractmethod
    def pushOn(self, queue, job):
        pass

    def createRedisPayload(self, job):
        return {
            'module': job.__module__,
            'data': job.payload,
            'id': time.time()
        }

    def createDatabasePayload(self, job):
        return {
            'module': job.__module__,
            'data': job.payload,
            'id': time.time()
        }
