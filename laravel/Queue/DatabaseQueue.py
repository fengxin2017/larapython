import json
from time import time

from laravel.Helps.Help import app
from .Queue import Queue


class DatabaseQueue(Queue):

    def laterOn(self, queue, delay, job):
        payload = self.createDatabasePayload(job)
        pass

    def pushOn(self, queue, job):
        payload = self.createDatabasePayload(job)
        pass
