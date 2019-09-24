import asyncio

from laravel.Helps.Help import viewResponse

class IndexController():
    async def index(self, request):
        await asyncio.sleep(1)

        name = request.get('name',default='haha')
        return viewResponse('i am {}'.format(name))
