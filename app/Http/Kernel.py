from laravel.Foundation.Http.Kernel import Kernel as HttpKernel


class Kernel(HttpKernel):
    Middleware = [
        'app.Http.Middleware.M1',
        'app.Http.Middleware.M2',
        'app.Http.Middleware.M3'
    ]
