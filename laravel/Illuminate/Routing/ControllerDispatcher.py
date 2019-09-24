class ControllerDispatcher():
    def __init__(self, app):
        self.app = app

    async def dispatch(self, route, request):
        cls, action = route.action.split('@')

        controller = self.app.make(route.namespace + '.' + cls)

        return await getattr(controller, action)(request)
