import sync


class ShouldQueue(metaclass=sync.ABCMeta):
    def __init__(self, payload={}):
        self.payload = payload
