from laravel.Illuminate.Helps.Help import app, current_config


class Request():
    def __init__(self, baseRequest):
        self.request = baseRequest

    def __getattr__(self, item):
        try:
            return getattr(self.request, item)
        except AttributeError:
            raise Exception('Method {} not exist'.format(item))

    def setRouteResolver(self, routeResolver):
        self.routeResolver = routeResolver

    def route(self):
        return self.routeResolver()

    def get(self, key=None, default=None):
        if key is None:
            return self.query
        if key in self.query.keys():
            return self.query[key]
        if default:
            return default
        raise Exception('key is invalid')

    async def posts(self, key=None, default=None):
        post = await self.post()
        if key is None:
            return post
        if key in post.keys():
            return post[key]
        if default:
            return default
        raise Exception('key is invalid')

    async def all(self):
        post = await self.post()

        return {**self.query, **post}

    async def files(self, name):
        post = await self.post()

        filename = post[name].filename

        ext = filename.split('.')[-1]

        content = post[name].file.read()

        return File(filename, ext, content)


class File():
    def __init__(self, filename, ext, content):
        self.filename = filename
        self.ext = ext
        self.content = content
        self.path = app().staticPath

    def store(self, path=None):
        import os
        if path:
            self.path += path.strip('/') + '/'

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(self.path + self.filename, 'wb') as f:
            f.write(self.content)

        return current_config('app.url').strip('/') + '/' + path.strip('/') + '/' + self.filename

    def storeAs(self, path=None, filename=None):
        if filename:
            self.filename = filename + '.' + self.ext

        return self.store(path=path)
