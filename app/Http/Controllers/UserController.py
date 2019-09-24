from app.Http.Controllers.Controller import Controller
from laravel.Helps.Help import app, jsonResponse, viewResponse
from app.Events.UserRegister import UserRegister
from random import randint
import asyncio
from functools import partial


class UserController(Controller):
    async def index(self, request):
        return viewResponse('<h1>UserController@index</h1>')

    async def event(self, request):
        # app('events').listen('app.Events.UserRegister', 'app.Listeners.UserRegisterListener')
        # UserRegister.dispatch({'name':'admin'})

        # print(app('events').listeners)
        # exit()


        # for _ in range(30):
        #     re = await app('events').dispatch('test', {'name': 'test'})
        #     re.add_done_callback(self.hello())

        # await UserRegister.dispatch({'name': 'admin'})
        # await app('events').dispatch(UserRegister({'name': 'foxirver'}))

        coros = [self.coro({'name': 'test'}) for _ in range(30)]

        future = asyncio.gather(*coros)

        future.add_done_callback(partial(self.hello, 'hello world'))

        return viewResponse('done')

    # async def t(self, payload):
    #     await UserRegister.dispatch(payload)

    async def coro(self, payload):
        sec = randint(1, 5)
        await asyncio.sleep(sec)
        print(payload, 'called with closure', sec)
        return sec

    def hello(self, world, future):
        print(future.result())
        print(world)

    async def config(self, request):
        configs = app('config').all()

        return jsonResponse(configs)
