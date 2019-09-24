from laravel.Illuminate.Bus.Dispatcher import Dispatcher
from laravel.Illuminate.Support.ServiceProvider import ServiceProvider


class BusServiceProvider(ServiceProvider):

    def register(self):
        print('|BusServiceProvider is registering to container')
        self.app.singleton('bus', self.__getBusDispatcherClosure())

    def __getBusDispatcherClosure(self):
        def closure(app):
            return Dispatcher(app, self.__setQueueResolver())

        return closure

    def __setQueueResolver(self):
        def queueResolvoer(driver):
            return self.app.make('queue.' + driver)

        return queueResolvoer

    def boot(self):
        self.app.make('bus')
        print('|BusServiceProvider booted')
