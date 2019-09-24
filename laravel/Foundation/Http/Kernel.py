from contextvars import ContextVar
from copy import deepcopy

from laravel.Pipeline.Pipeline import Pipeline

# currentApp = ContextVar('currentApp')

currentRequest = ContextVar('currentRequest')

currentConfig = ContextVar('current.config')


class Kernel():
    Bootstrappers = [
        'laravel.Foundation.Bootstrap.LoadConfiguration',
        'laravel.Foundation.Bootstrap.RegisterProviders',
        'laravel.Foundation.Bootstrap.BootProviders'
    ]

    def __init__(self, app, router):
        self.app = app
        self.router = router

    async def handle(self, request):
        from laravel.Helps.Help import app

        self._initCurrentConfig(deepcopy(app('config')))

        self._initCurrentRequest(request)

        # self._initCurrentApp(deepcopy(app()))

        return await self.sendRequestThroughRouter(request)

    def _initCurrentConfig(self,config):
        currentConfig.set(config)

    def _initCurrentRequest(self, request):
        currentRequest.set(request)

    # def _initCurrentApp(self,app):
    #     currentApp.set(app)

    async def sendRequestThroughRouter(self, request):
        return await Pipeline(self.app).send(request).through(self.Middleware).then(self.dispatchToRouter())

    def dispatchToRouter(self):
        async def closure(request):
            return await self.router.dispatch(request)

        return closure

    def bootstrap(self):
        if not self.app.hasBeenBootstrapped:
            self.app.bootstrapWith(self.Bootstrappers);

        return self

    def getApplication(self):
        return self.app
