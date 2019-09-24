class M2():
    async def handle(self, request, next):
        print('m2', request)
        return await next(request)
