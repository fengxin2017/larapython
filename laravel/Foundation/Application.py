import importlib
import os

from laravel.Events.EventServiceProvider import EventServiceProvider
from laravel.Logs.LogServiceProvider import LogServiceProvider
from laravel.Routing.RoutingServiceProvider import RoutingServiceProvider


class Application():
    Instance = None

    def __init__(self, basePath):

        self.setPath(basePath)

        self.initProperty()

        self.registerBaseBindings()

        self.registerBaseServiceProviders()

    def initProperty(self):
        self.bindings = dict()
        self.serviceProviders = list()
        self.resolved = dict()
        self.instances = dict()
        self.reboundCallbacks = dict()
        self.booted = False
        self.hasBeenBootstrapped = False

    def setPath(self, basePath):
        self.basePath = basePath
        self.setAppPath(basePath)
        self.setPublicPath(basePath)
        self.setStoragePath(basePath)
        self.setLogPath()
        self.setStaticPath()

    def setAppPath(self, basePath):
        self.appPath = basePath + 'app/'

    def setPublicPath(self, basePath):
        self.publicPath = basePath + 'public/'

    def setStoragePath(self, basePath):
        self.storagePath = basePath + 'storage/'
        if not os.path.exists(self.storagePath):
            os.makedirs(self.storagePath)

    def setLogPath(self):
        self.logPath = self.storagePath + 'Logs/'
        if not os.path.exists(self.logPath):
            os.makedirs(self.logPath)

    def setStaticPath(self):
        self.staticPath = self.storagePath + 'static/'
        if not os.path.exists(self.staticPath):
            os.makedirs(self.staticPath)

    def registerBaseBindings(self):
        self.setInstance(self)
        self.instances['app'] = self

    def registerBaseServiceProviders(self):
        self.register(EventServiceProvider(self))
        self.register(LogServiceProvider(self))
        self.register(RoutingServiceProvider(self))

    def bootstrapWith(self, bootstrappers):
        self.hasBeenBootstrapped = True

        for bootstrapper in bootstrappers:
            self.make(bootstrapper).bootstrap(self)

    def register(self, provider):

        provider.register();

        self.markAsRegistered(provider)

        if self.booted:
            self.bootProvider(provider)

        return provider

    def markAsRegistered(self, provider):
        self.serviceProviders.append(provider);

    def bind(self, abstract=None, concrete=None, shared=False):
        self.dropStaleInstances(abstract)

        self.bindings[abstract] = {
            'concrete': concrete,
            'shared': shared
        }

        if self.hasResolved(abstract):
            self.rebound(abstract)

    def dropStaleInstances(self, abstract):
        if abstract in self.instances.keys():
            self.instances.pop(abstract)

    def hasResolved(self, abstract):
        return abstract in self.resolved.keys() or abstract in self.instances.keys()

    def bound(self, abstract):
        return abstract in self.bindings.keys() or abstract in self.instances.keys()

    def rebound(self, abstract):
        instance = self.make(abstract)

        for callback in self.getReboundCallbacks(abstract):
            callback(self, instance)

    def getReboundCallbacks(self, abstract):
        if abstract in self.reboundCallbacks.keys():
            return self.reboundCallbacks[abstract]

        return list()

    def make(self, abstract, *args, **kwargs):
        if abstract in self.instances.keys():
            return self.instances[abstract]

        if abstract in self.bindings.keys():
            object = self.bindings[abstract]['concrete'](self, *args, **kwargs)

            if self.isShared(abstract):
                self.instances[abstract] = object

            self.resolved[abstract] = True

            return object

        return self.build(abstract, *args, **kwargs)

    def isShared(self, abstract):
        return abstract in self.instances.keys() or (abstract in self.bindings and self.bindings[abstract]['shared'])

    def build(self, abstract, *args, **kwargs):
        module = importlib.import_module(abstract)

        return getattr(module, abstract.split('.')[-1])(*args, **kwargs)

    def singleton(self, abstract, concrete):
        self.bind(abstract, concrete, True)

    def instance(self, abstract, instance):
        isBound = self.bound(abstract)

        self.instances[abstract] = instance

        if isBound:
            self.rebound(abstract)

    def forgetInstance(self, abstract):
        if abstract in self.instances.keys():
            del self.instances[abstract]

    def forgetInstances(self):
        self.instances = dict()

    def forgetResolved(self, abstract):
        if abstract in self.resolved.keys():
            del self.resolved[abstract]

    def forgetResolves(self):
        self.resolved = dict()

    def flush(self):
        pass

    def rebinding(self, abstract, callback):
        if abstract not in self.reboundCallbacks.keys():
            self.reboundCallbacks[abstract] = list()

        self.reboundCallbacks[abstract].append(callback)

        if self.bound(abstract):
            return self.make(abstract)

    def refresh(self, abstract, target, method):
        return self.rebinding(abstract, self.__getRebindingClosure(target, method));

    def __getRebindingClosure(self, target, method):
        def closure(app, instance):
            return getattr(target, method)(instance)

        return closure

    def setInstance(self, app):
        Application.Instance = app

    def getInstance(self):
        return Application.Instance

    def boot(self):
        print('------------------------------------------------')
        print('|start boot ServiceProviders                   |')
        print('------------------------------------------------')
        if self.booted:
            return

        for provider in self.serviceProviders:
            self.bootProvider(provider)

        self.booted = True;
        print('------------------------------------------------')
        print('|ServiceProviders haveBeenBooted               |')
        print('------------------------------------------------')
        print('-------------------resolved---------------------')
        for reslove in self.resolved:
            print('| ' + reslove.ljust(45) + '|')
        print('------------------------------------------------')
        print('-------------------instances--------------------')
        for instance in self.instances:
            print('| ' + instance.ljust(45) + '|')
        print('------------------------------------------------')
        print('-------------------bindings---------------------')
        for bingding, values in self.bindings.items():
            print('| ' + bingding.ljust(30), '【singleton】' if values['shared'] else '【bind】', '|')
        print('------------------------------------------------')

    def bootProvider(self, provider):
        provider.boot()

    def registerConfiguredProviders(self):
        print('------------------------------------------------')
        print('|start register other ServiceProviders         |')
        print('------------------------------------------------')
        providers = self.make('config').get('app.providers')

        if providers and len(providers):
            for provider in providers:
                serviceProvider = self.make(provider, self)
                self.register(serviceProvider)
        print('------------------------------------------------')
        print('|other ServiceProviders havebeen registed      |')
        print('------------------------------------------------')
        return

    def decorator(self):
        def getClosure(func):
            def closure(*args, **kwargs):
                return func(*args, **kwargs)

            return closure

        return getClosure
