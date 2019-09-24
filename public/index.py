import asyncio
import datetime
import os
import sys
import time
import traceback

from aiohttp import web

sys.path.append('/larapy/venv/Lib/site-packages')
sys.path.append('../')



from app.Http.Kernel import Kernel

from laravel.Http.Request import Request
from laravel.Exception.NotFoundException import NotFoundException
from laravel.Helps.Help import viewResponse


def getKernelClosure(router):
    def closure(app):
        return Kernel(app, router)

    return closure


class Server():
    def __init__(self, kernel):
        self.kernel = kernel
        self.loop = asyncio.get_event_loop()
        app().instance('loop', self.loop)
        self.loop.create_task(self.run())

    async def handler(self, request):
        try:
            request = Request(request)

            return await self.kernel.handle(request);
        except NotFoundException:
            with open('../laravel/Foundation/Exceptions/404.html') as f:
                body = f.read()

            return web.Response(body=body, status=404, content_type='text/html')
        except BaseException as e:
            today = datetime.date.today()

            if app('config').get('app.log'):
                with open(app().logPath + str(today) + '.log', 'a') as f:
                    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    f.write('【TIME】  ' + now + '\n')
                    traceback.print_exc(file=f)
                    f.write('\n\n')

            if app('config').get('app.trace'):
                traceback.print_exc()

            if app('config').get('app.debug'):
                ex = traceback.format_exc().splitlines()
                body = '<br/>'.join(ex)
                return web.Response(body=body, status=500, content_type='text/html')

            return web.Response(body='服务器异常', status=500, content_type='text/html', charset='utf-8')
        finally:
            pass

    async def run(self):
        server = web.Server(self.handler)
        await self.loop.create_server(server, "0.0.0.0", 8899)


if __name__ == '__main__':

    from laravel.Helps.Help import Application, app

    application = Application(os.getcwd() + '/../')

    application.singleton('kernel', getKernelClosure(app('router')))

    kernel = app('kernel').bootstrap()

    server = Server(kernel)

    try:
        server.loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.loop.close()
