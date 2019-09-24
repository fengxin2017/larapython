from laravel.Support.ServiceProvider import ServiceProvider


class RouteServiceProvider(ServiceProvider):
    def boot(self):
        self.loadRoutes()

    def loadRoutes(self):
        if self.map:
            self.map()
