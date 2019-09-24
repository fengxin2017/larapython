import importlib
import os

from laravel.Config.Repository import Repository


class LoadConfiguration():
    def bootstrap(self, app):
        configDir = app.basePath + '/config'

        filenames = list()

        for root, dirs, files in os.walk(configDir):
            if len(files):
                filenames = files
                break

        configs = dict()

        for filename in filenames:
            abstract = filename.replace('.py', '')
            module = importlib.import_module('config.' + abstract)
            if abstract not in configs.keys():
                configs[abstract] = dict()

            for var in dir(module):
                if not var.startswith('__'):
                    configs[abstract][var] = getattr(module, var)

        app.instance('config', Repository(configs))

        # e.g.

        # print(current_config('database.mysql.prefix','admin'))
        #
        # print(current_config('database.mysql.password','55555'))
        #
        # print(current_config())

        # confs = app.make('config')
        #
        # confs.set('admin.age','23')
        #
        # confs.get('admin.age')
        #
        # print(confs.items)
