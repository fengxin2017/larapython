from laravel.Helps.Help import viewResponse
class M1():
    async def handle(self, request, next):
        print('m1', request)
        # return viewResponse('hahahah')

        return await next(request)
