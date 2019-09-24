import time
import abc


class Queue(metaclass=abc.ABCMeta):
    def __init__(self, app):
        self.app = app

    @abc.abstractmethod
    def laterOn(self, queue, delay, job):
        pass

    @abc.abstractmethod
    def pushOn(self, queue, job):
        pass

    def createRedisPayload(self, job):
        return {
            'module': job.__module__,
            'payload': job.payload,
            'id': time.time()
        }

    def createDatabasePayload(self, job):
        return {
            'module': job.__module__,
            'payload': job.payload,
            'id': time.time()
        }
