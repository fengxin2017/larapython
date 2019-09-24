from laravel.Support.ServiceProvider import ServiceProvider
from laravel.Helps.Help import app


class EventServiceProvider(ServiceProvider):
    items = {}

    def boot(self):
        for event, listener in self.items.items():
            if isinstance(listener, str):
                app('events').listen(event, listener)
            if isinstance(listener, list):
                for item in listener:
                    app('events').listen(event, item)

        print('| Support EventServiceProvider booted')
