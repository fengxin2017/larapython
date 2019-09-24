import redis

from laravel.Illuminate.Support.ServiceProvider import ServiceProvider


class RedisServiceProvider(ServiceProvider):
    def register(self):
        print('|RedisServiceProvider is registering to container')
        self.app.singleton('redis', self.getRedisClosure())
        self.app.singleton('redis.pool', self.getRedisPoolClosure())

    def getRedisClosure(self):
        host, port = self.getHostPort()

        def closure(app):
            return redis.Redis(host=host, port=port, decode_responses=True)

        return closure

    def getRedisPoolClosure(self):
        def closure(app):
            pool = self.getPool()
            return redis.Redis(connection_pool=pool)

        return closure

    def getPool(self):
        host, port = self.getHostPort()

        return redis.ConnectionPool(host=host, port=port, decode_responses=True)

    def getHostPort(self):
        return (self.app.make('config').get('database.redis.host'), self.app.make('config').get('database.redis.port'))

    def boot(self):
        print('-----ready to start redis|pool-------')
        self.app.make('redis')
        self.app.make('redis.pool')
        print('-----redis|pool has been started-----')
        print('|RedisServiceProvider booted')
