class Route():
    def __init__(self, method, uri, attributes):
        self.method = method
        self.uri = uri
        self.request = None

        if 'action' not in attributes.keys():
            raise Exception('action missed in route')
        else:
            self.action = attributes['action']

        if 'namespace' not in attributes.keys():
            raise Exception('namespace missed in route')
        else:
            self.namespace = attributes['namespace']

        if 'Middleware' not in attributes.keys():
            self.middleware = list()
        else:
            self.middleware = attributes['Middleware']

    def matches(self, request):
        requestUri = request.path

        if requestUri == self.uri or requestUri + '/' == self.uri:
            return self

    async def run(self, request):

        return await self.runController(request)

    async def runController(self, request):
        return await self.app.make('controllerDispatcher').dispatch(self, request)

    def setRouter(self, router):
        self.router = router
        return self

    def setContainer(self, app):
        self.app = app
        return self
