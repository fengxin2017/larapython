from laravel.Illuminate.Queue.CallQueuedHandler import CallQueuedHandler
from laravel.Illuminate.Queue.Worker import Worker
from laravel.Illuminate.Support.ServiceProvider import ServiceProvider


class QueueServiceProvider(ServiceProvider):

    def register(self):
        print('|QueueServiceProvider is registering to container')
        self.registerDefaultQueue()
        self.registerSupportedQueues()
        self.registerWorker()
        self.registerCallQueuedHandler()

    def registerDefaultQueue(self):
        defaultDriver = self.getDefaultDriver()

        queueDefaultModule = self.getQueueModuleByDriver(defaultDriver)

        self.app.singleton('queue', self.getQueueClosure(queueDefaultModule))

    def getDefaultDriver(self):
        return self.app.make('config').get('queue.default')

    def getQueueModuleByDriver(self, driver):
        return self.app.make('config').get('queue.drivers.' + driver + '.use')

    def getQueueClosure(self, queueModule):
        def closure(app):
            return app.make(queueModule, app)

        return closure

    def registerSupportedQueues(self):
        for driver in self.getSupportedDrivers():
            module = self.getQueueModuleByDriver(driver)
            self.app.singleton('queue.' + driver, self.getQueueClosure(module))

    def getSupportedDrivers(self):
        return self.app.make('config').get('queue.drivers')

    def registerWorker(self):
        self.app.singleton('worker', self.getWorkerClosure())

    def getWorkerClosure(self):
        def closure(app):
            return Worker(app)

        return closure

    def registerCallQueuedHandler(self):
        self.app.singleton('callQueueHandler', self.getCallQueuedHandler())

    def getCallQueuedHandler(self):
        def closure(app):
            return CallQueuedHandler(app)

        return closure

    def boot(self):
        self.app.make('queue')
        for driver in self.getSupportedDrivers():
            self.app.make('queue.' + driver)

        print('|QueueServiceProvider booted')
