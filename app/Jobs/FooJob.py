import asyncio

from laravel.Foundation.Bus.ShouldQueue import ShouldQueue


class FooJob(ShouldQueue):
    async def handle(self, payload):
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        await asyncio.sleep(3)
        print('finished', payload)
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        # print(payload['name'] + '结束')
