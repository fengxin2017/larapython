from functools import reduce


class Pipeline():
    def __init__(self, app):
        self.app = app

    def send(self, passable):
        self.passable = passable

        return self

    def through(self, pipes):
        self.pipes = pipes

        return self

    async def then(self, destination):
        runer = reduce(self.carry(), list(reversed(self.pipes)), self.prepareDestination(destination))

        return await runer(self.passable)

    def prepareDestination(self, destination):
        async def closure(passable):
            return await destination(passable)

        return closure

    def carry(self):
        def wrapper(stack, pipe):
            async def inner(passable):
                return await self.app.make(pipe).handle(passable, stack)

            return inner

        return wrapper
