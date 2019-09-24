class RouteRegistrar():
    passthru = [
        'get', 'post', 'put', 'patch', 'delete', 'options', 'any',
    ]

    allowedAttributes = [
        'as', 'domain', 'middleware', 'name', 'namespace', 'prefix', 'where',
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
            # 用list对middleware进行一次浅拷贝，避免当前对象attributes['middleware']和router的buildStack['middleware']指向同一地址造成重复加载中间件
            'middleware':
                list(router.buildStack['middleware'][-1])
                if 'middleware' in router.buildStack.keys() and len(router.buildStack['middleware'])
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

        if 'middleware' in attributes.keys() and len(attributes['middleware']) > 0:
            self.attributes['middleware'] += attributes['middleware']

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
