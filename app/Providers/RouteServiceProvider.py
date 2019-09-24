from laravel.Foundation.Support.ServiceProviders.RouteServiceProvider import RouteServiceProvider as ServiceProvider

from routes.web import web, foo, example
from routes.api import api

from laravel.Helps.Help import app


class RouteServiceProvider(ServiceProvider):
    def boot(self):
        super().boot()
        print('|RouteSerivceProvider booted')

    def map(self):
        self.mapApiRoutes()
        self.mapWebRoutes()

    def mapApiRoutes(self):
        api(app('router'))

    def mapWebRoutes(self):
        web(app('router'))
        foo(app('router'))
        example(app('router'))
