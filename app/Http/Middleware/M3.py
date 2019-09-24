class M3():
    async def handle(self, request, next):
        print('m3', request)
        return await next(request)
