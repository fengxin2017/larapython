from random import randint
from laravel.Foundation.Bus.ShouldQueue import ShouldQueue
import asyncio


class UserRegisterListener(ShouldQueue):
    async def handle(self, payload):
        sec = randint(1, 5)
        await asyncio.sleep(sec)
        print(payload, '------', sec)
        return 'userregister {}'.format(sec)
