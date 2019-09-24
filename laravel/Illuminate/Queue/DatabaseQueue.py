import json
from time import time

from laravel.Illuminate.Helps.Help import app
from laravel.Illuminate.Queue.Queue import Queue


class DatabaseQueue(Queue):

    def laterOn(self, queue, delay, job):
        payload = self.createDatabasePayload(job)
        pass

    def pushOn(self, queue, job):
        payload = self.createDatabasePayload(job)
        pass
