class RouteRegistrar():
    passthru = [
        'get', 'post', 'put', 'patch', 'delete', 'options', 'any',
    ]

    allowedAttributes = [
        'as', 'domain', 'Middleware', 'name', 'namespace', 'prefix', 'where',
    ]

    def __init__(self, router):
        self.router = router
        self.attributes = {
            'action': str(),
            'prefix':
                '/' + router.buildStack['prefix'][-1].strip('/')
                if 'prefix' in router.buildStack.keys() and len(router.buildStack['prefix'])
                else '',
            'namespace':
                router.buildStack['namespace'][-1]
                if 'namespace' in router.buildStack.keys() and len(router.buildStack['namespace'])
                else '',
            # 用list对middleware进行一次浅拷贝，避免当前对象attributes['Middleware']和router的buildStack['Middleware']指向同一地址造成重复加载中间件
            'Middleware':
                list(router.buildStack['Middleware'][-1])
                if 'Middleware' in router.buildStack.keys() and len(router.buildStack['Middleware'])
                else list()
        }

    def setAttributes(self, attributes):
        if 'prefix' in attributes.keys():
            prefix = attributes['prefix'].strip('/')
            if prefix:
                self.attributes['prefix'] += '/%s' % prefix

        if 'namespace' in attributes.keys() and attributes['namespace']:
            if self.attributes['namespace']:
                self.attributes['namespace'] += '.%s' % attributes['namespace']
            else:
                self.attributes['namespace'] += attributes['namespace']

        if 'Middleware' in attributes.keys() and len(attributes['Middleware']) > 0:
            self.attributes['Middleware'] += attributes['Middleware']

        return self

    def attribute(self, key, value):
        self.attributes[key] = value

    def get(self, uri, action):
        self.attribute('action', action)
        uri = self.attributes['prefix'] + '/' + uri.strip('/')
        return self.router.get(uri, self.attributes)

    def post(self, uri, action):
        self.attribute('action', action)
        uri = self.attributes['prefix'] + '/' + uri.strip('/')
        return self.router.post(uri, self.attributes)
