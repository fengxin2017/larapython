from laravel.Illuminate.Routing.ControllerDispatcher import ControllerDispatcher
from laravel.Illuminate.Routing.Router import Router
from laravel.Illuminate.Support.ServiceProvider import ServiceProvider

class RoutingServiceProvider(ServiceProvider):
    def __init__(self, app):
        self.app = app

    def register(self):
        print('|RoutingServiceProvider is registering to container')
        self.registerRouter();
        self.registerControllerDispatcher();

    def registerRouter(self):
        self.app.singleton('router', self.getRouterClosure());

    def registerControllerDispatcher(self):
        self.app.singleton('controllerDispatcher', self.getControllerDispatcher());

    def getRouterClosure(self):
        def closure(app):
            return Router(app.make('events'), app)

        return closure

    def getControllerDispatcher(self):
        def closure(app):
            return ControllerDispatcher(app)

        return closure

    def boot(self):
        self.app.make('controllerDispatcher')
        print('|RoutingServiceProvider booted')
