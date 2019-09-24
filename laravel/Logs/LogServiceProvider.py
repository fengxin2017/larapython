from laravel.Support.ServiceProvider import ServiceProvider


class LogServiceProvider(ServiceProvider):
    def __init__(self, app):
        self.app = app

    def register(self):
        print('|LogServiceProvider is registering to container')
        pass

    def boot(self):
        print('|LogServiceProvider booted')
