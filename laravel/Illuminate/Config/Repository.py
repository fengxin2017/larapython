class Repository():
    def __init__(self, items={}):
        self.items = items

    def has(self, key):
        try:
            self.get(key)
            return True
        except:
            return False

    def get(self, key, default=None):
        items = self.items

        sugments = key.split('.')

        for sugment in sugments:
            if sugment in items.keys():
                items = items[sugment]
            elif default:
                return default
            else:
                raise Exception('invalid key {}'.format(key))
        return items

    def set(self, key, value):
        keys = key.split('.')

        items = self.items

        while len(keys) > 1:
            key = keys.pop(0)

            if key not in items.keys():
                items[key] = dict()
            items = items[key]

        items[keys.pop()] = value

        return self

    def all(self):
        return self.items
