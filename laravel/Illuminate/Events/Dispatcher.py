from laravel.Illuminate.Foundation.Bus.ShouldQueue import ShouldQueue
from laravel.Illuminate.Foundation.Events.Dispatchable import Dispatchable


class Dispatcher():
    def __init__(self, app):
        self.app = app
        self.queueResolver = None
        self.listeners = {}

    def listen(self, events, listener):
        if isinstance(events, str):
            self.listeners[events] = self.makeListener(listener)
        if isinstance(events, list):
            for event in events:
                self.listeners[event] = self.makeListener(listener)

    def makeListener(self, listener):
        if isinstance(listener, str):
            return self.createClassListener(listener)
        return listener

    def createClassListener(self, listener):
        from laravel.Illuminate.Helps.Help import app, tap
        def closure(parameters):
            listenerObj = tap(self.app.make(listener), self.setPayload(parameters))

            if isinstance(listenerObj, ShouldQueue):
                return app('bus').dispatch(listenerObj)
            return getattr(listenerObj, 'handle')(parameters)

        return closure

    def setPayload(self, parameters):
        def closure(obj):
            obj.payload = parameters

        return closure

    def dispatch(self, event, parameters={}):
        eventName, payload = self.parseEventAndPayload(event, parameters)

        if eventName in self.listeners.keys():
            return self.listeners[eventName](payload)
        raise Exception(eventName + ' is invalid')

    def parseEventAndPayload(self, event, parameters):
        if isinstance(event, Dispatchable):
            return (event.eventName, event.payload)
        return (event, parameters)
