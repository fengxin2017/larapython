from laravel.Foundation.Support.ServiceProviders.EventServiceProvider import EventServiceProvider as ServiceProvider
from random import randint
import asyncio

class EventServiceProvider(ServiceProvider):
    items = {
        'app.Events.UserRegister': [
            'app.Listeners.UserRegisterListener',
            'app.Listeners.SendEmailListener'
        ]
    }

    def boot(self):
        self.app.make('events').listen('app.Events.UserRegister', self.userRegister())
        self.app.make('events').listen('test',self.userRegister())
        super().boot()

    def userRegister(self):
        async def closure(payload):
            sec = randint(1, 5)
            await asyncio.sleep(sec)
            print(payload, 'called with closure', sec)
            return sec

        return closure