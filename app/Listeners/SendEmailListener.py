from random import randint
from laravel.Foundation.Bus.ShouldQueue import ShouldQueue
import asyncio


class SendEmailListener():
    async def handle(self, payload):
        sec = randint(1, 5)
        await asyncio.sleep(sec)
        if sec % 2 == 0:
            raise Exception('error')
        print(payload, 'this is send emailListener', sec)
        return 'sendEmail {}'.format(sec)
