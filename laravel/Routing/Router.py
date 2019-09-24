from laravel.Pipeline.Pipeline import Pipeline
from .Route import Route
from .RouteCollection import RouteCollection
from .RouteRegistrar import RouteRegistrar


class Router():
    def __init__(self, events, app):
        self.events = events
        self.app = app
        self.routes = RouteCollection()
        self.buildStack = {
            'namespace': list(),
            'prefix': list(),
            'Middleware': list()
        }

    def getRoutes(self):
        return self.routes;

    async def dispatch(self, request):
        return await self.dispatchToRoute(request)

    async def dispatchToRoute(self, request):
        return await self.runRoute(request, self.findRoute(request))

    def findRoute(self, request):
        return self.routes.match(request)

    async def runRoute(self, request, route):
        request.setRouteResolver(self.getRouteResolverClosure(route))

        return await self.runRouteWithinStack(route, request)

    def getRouteResolverClosure(self, route):
        def closure():
            return route

        return closure

    async def runRouteWithinStack(self, route, request):
        middleware = self.gatherRouteMiddleware(route)
        return await Pipeline(self.app).send(request).through(middleware).then(self.getRunClosure(route))

    def gatherRouteMiddleware(self, route):
        return route.middleware

    def getRunClosure(self, route):

        async def closure(request):
            return await self.toResponse(request, await route.run(request))

        return closure

    async def toResponse(self, request, response):
        return response

    def get(self, uri, attributes):
        if isinstance(attributes, str):
            attrs = self._getDefaultAttr(attributes)

            uri = attrs['prefix'] + '/' + uri.strip('/')

            return self.addRoute('GET', uri, attrs)

        elif isinstance(attributes, dict):
            return self.addRoute('GET', uri, attributes)

    def post(self, uri, attributes):
        if isinstance(attributes, str):

            attrs = self._getDefaultAttr(attributes)

            uri = attrs['prefix'] + '/' + uri.strip('/')

            return self.addRoute('POST', uri, attrs)
        elif isinstance(attributes, dict):
            return self.addRoute('POST', uri, attributes)

    def _getDefaultAttr(self, action):
        return {
            'action': action,
            'prefix':
                '/' + self.buildStack['prefix'][-1].strip('/')
                if 'prefix' in self.buildStack.keys() and len(self.buildStack['prefix'])
                else '',
            'namespace':
                self.buildStack['namespace'][-1]
                if 'namespace' in self.buildStack.keys() and len(self.buildStack['namespace'])
                else '',
            # 用list对middleware进行一次浅拷贝，避免当前对象attributes['Middleware']和router的buildStack['Middleware']指向同一地址造成重复加载中间件
            'Middleware':
                list(self.buildStack['Middleware'][-1])
                if 'Middleware' in self.buildStack.keys() and len(self.buildStack['Middleware'])
                else list()
        }

    def addRoute(self, method, uri, attributes):
        return self.routes.add(self.createRoute(method, uri, attributes))

    def createRoute(self, method, uri, attributes):
        return self.newRoute(method, uri, attributes)

    def newRoute(self, method, uri, attributes):
        return Route(method, uri, attributes).setRouter(self).setContainer(self.app)

    def attr(self, attributes):
        return RouteRegistrar(self).setAttributes(attributes)

    def namespace(self, namespace):
        def Closure(func):
            def inner(router):
                router.buildStack['namespace'].append(namespace)
                func(router)
                router.buildStack['namespace'].pop()

            return inner

        return Closure

    def prefix(self, prefix):
        def Closure(func):
            def inner(router):
                router.buildStack['prefix'].append(prefix)
                func(router)
                router.buildStack['prefix'].pop()

            return inner

        return Closure

    def middleware(self, middleware):
        def Closure(func):
            def inner(router):
                router.buildStack['Middleware'].append(middleware)
                func(router)
                router.buildStack['Middleware'].pop()

            return inner

        return Closure
