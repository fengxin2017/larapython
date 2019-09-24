class M5():
    async def handle(self, request, next):
        print('m5 is controller Middleware')
        return await next(request)