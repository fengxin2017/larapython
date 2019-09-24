import asyncio
class M4():
    async def handle(self, request, next):
        # await asyncio.sleep(0.5)
        print('m4 is group Middleware')
        return await next(request)