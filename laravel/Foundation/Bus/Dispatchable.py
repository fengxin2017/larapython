from .PendingDispatch import PendingDispatch


class Dispatchable():
    def __init__(self, payload={}):
        self.payload = payload

    @classmethod
    def dispatch(cls, payload={}):
        return PendingDispatch(cls(payload=payload))
