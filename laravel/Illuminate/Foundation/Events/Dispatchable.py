class Dispatchable():
    def __init__(self, payload={}):
        self.payload = payload
        self.eventName = self.__module__

    @classmethod
    def dispatch(cls, payload={}):
        from laravel.Illuminate.Helps.Help import app

        return app('events').dispatch(cls(payload=payload))

