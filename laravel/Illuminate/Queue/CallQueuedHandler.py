import json


class CallQueuedHandler():
    def __init__(self, app):
        self.app = app

    async def call(self, job):
        try:
            job = self.parseJsonToOriginDict(job)
            await self.app.make(job['module'], job['data']).handle(job['data'])
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            exit()

    def parseJsonToOriginDict(self, job):
        return json.loads(job)
