from laravel.Exception.NotFoundException import NotFoundException


class RouteCollection():
    def __init__(self):
        self.routes = dict()

    def match(self, request):
        routes = self.groupBy(request.method)

        route = self.__matchAgainstRoutes(routes, request)

        if route:
            return route

        raise NotFoundException()

    def groupBy(self, method=None):

        if not method:
            return self.routes
        return self.routes[method]

    def __matchAgainstRoutes(self, routes, request):
        for route in routes:
            if route.matches(request):
                return route
        return None

    def add(self, route):
        self.addToCollections(route)
        return route

    def addToCollections(self, route):
        if route.method not in self.routes.keys():
            self.routes[route.method] = list()

        for item in self.routes[route.method]:
            if item.uri == route.uri:
                self.routes[route.method].remove(item)

        self.routes[route.method].append(route)

    # 通过name获取路由
    def getByName(self):
        pass

    def getRoutes(self):
        return self.routes

    def setRoutes(self, routes):
        self.routes = routes
        return self
