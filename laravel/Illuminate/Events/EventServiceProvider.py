from laravel.Illuminate.Events.Dispatcher import Dispatcher
from laravel.Illuminate.Support.ServiceProvider import ServiceProvider


class EventServiceProvider(ServiceProvider):

    def register(self):
        print('|EventServiceProvider is registering to container')
        self.app.singleton('events', self.__getEventDispatcherClosure())

    def __getEventDispatcherClosure(self):
        def closure(app):
            return Dispatcher(app)

        return closure

    def boot(self):
        print('|EventServiceProvider booted')