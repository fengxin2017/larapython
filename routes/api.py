from laravel.Helps.Help import app

router = app('router')

@router.namespace('app.Http.Controllers.Api')
@router.prefix('/Api')
def api(router):
    router.get('/index', 'IndexController@index')

