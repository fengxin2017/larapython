from laravel.Foundation.Bus.ShouldQueue import ShouldQueue
from laravel.Foundation.Events.Dispatchable import Dispatchable
import asyncio


class Dispatcher():
    def __init__(self, app):
        self.app = app
        self.queueResolver = None
        self.listeners = {}

    def listen(self, events, listener):
        if isinstance(events, str):
            self.__listenOne(events, listener)

        if isinstance(events, list):
            self.__listenMany(events, listener)

    def __listenOne(self, event, listener):
        if event not in self.listeners.keys():
            self.listeners[event] = []
        self.listeners[event].append(self.makeListener(listener))

    def __listenMany(self, events, listener):
        for event in events:
            if event not in self.listeners.keys():
                self.listeners[event] = []
            self.listeners[event].append(self.makeListener(listener))

    def makeListener(self, listener):
        if isinstance(listener, str):
            return self.createClassListener(listener)
        return listener

    def createClassListener(self, listener):
        from laravel.Helps.Help import app, tap
        async def closure(payload):
            listenerObj = tap(self.app.make(listener), self.setPayload(payload))

            if isinstance(listenerObj, ShouldQueue):
                return await app('bus').dispatch(listenerObj)
            return await getattr(listenerObj, 'handle')(payload)

        return closure

    def setPayload(self, payload):
        def closure(obj):
            obj.payload = payload

        return closure

    async def dispatch(self, event, parameters={}, returnExceptions=False):
        eventName, payload = self.parseEventAndPayload(event, parameters)

        if eventName in self.listeners.keys():
            tasks = [asyncio.create_task(self.createCoro(listener, payload)) for listener in self.listeners[eventName]]
            return (asyncio.gather(*tasks, return_exceptions=returnExceptions), tasks)

    async def createCoro(self, listener, payload):
        return await listener(payload)

    def parseEventAndPayload(self, event, parameters):
        if isinstance(event, Dispatchable):
            return (event.eventName, event.payload)
        return (event, parameters)
