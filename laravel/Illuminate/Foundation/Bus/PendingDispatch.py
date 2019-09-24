class PendingDispatch():
    def __init__(self, job):
        self.job = job

    def delay(self, delay):
        self.job.delay = delay
        return self

    def onQueue(self, queue):
        self.job.queue = queue
        return self

    def driver(self, driver):
        self.job.driver = driver

    def __del__(self):
        from laravel.Illuminate.Helps.Help import app
        return app('bus').dispatch(self.job)
