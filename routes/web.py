from laravel.Helps.Help import app

router = app('router')


@router.namespace('app.Http.Controllers')
@router.middleware(['app.Http.Middleware.M4'])
def web(router):
    # router.attr({
    #     'Middleware': ['app.Http.Middleware.M4', 'app.Http.Middleware.M5']
    # }).get('home', 'HomeController@index')

    router.get('/','HomeController@index')

    router.get('home', 'HomeController@index')

    router.attr({
        'Middleware': ['app.Http.Middleware.M5']
    }).post('home', 'HomeController@index')

    router.get('/h', 'HomeController@home')

    router.get('/post', 'PostController@index')

    router.get('/queue', 'HomeController@queue')

    router.get('/user', 'UserController@index')

    #router.get('/event','UserController@event')

    router.get('', 'HomeController@index')

    router.get('/config','UserController@config')

    # print(router.routes.routes)
    # exit()

@router.namespace('app.Http.Controllers')
@router.middleware(['app.Http.Middleware.M4'])
def foo(router):
    router.get('foo','HomeController@foo')

    router.get('qiniu','HomeController@qiniu')

@router.namespace('app.Http.Controllers.Example')
def example(router):
    router.get('/event','EventController@index')
