import json
from time import time

from .Queue import Queue


class RedisQueue(Queue):

    def laterOn(self, queue, delay, job):
        payload = self.createRedisPayload(job)

        self.app.make('redis').zadd('queue:' + queue + ':delayed', self.__createPayloadForRedis(payload, delay))

    def pushOn(self, queue, job):
        payload = self.createRedisPayload(job)

        self.app.make('redis').zadd('queue:' + queue + ':delayed', self.__createPayloadForRedis(payload))

    def __createPayloadForRedis(self, payload, delay=0):
        return {
            json.dumps(payload): int(time()) + delay
        }
