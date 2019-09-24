import json

from laravel.Illuminate.Foundation.Application import Application
from laravel.Illuminate.Foundation.Http.Kernel import currentConfig, currentRequest
from laravel.Illuminate.Http.Response import Response


def tap(value, callback):
    callback(value);

    return value;


def app(abstract=None):
    if abstract == None:
        return Application.Instance
    return Application.Instance.make(abstract)

async def current_request(abstract=None, default=None, method=None):
    request = currentRequest.get()

    get = request.query

    post = await request.post()

    if abstract is None:
        return request

    if abstract in get.keys() and method == 'GET':
        return get[abstract]

    if abstract in post.keys() and method == 'POST':
        return post[abstract]

    if default:
        return default

    raise Exception('invalid key')


def current_config(abstract=None, value=None, default=None):
    conf = currentConfig.get()

    if abstract == None:
        return conf.all()

    if value == None:
        return conf.get(abstract, default)

    newConf = conf.set(abstract, value)

    return currentConfig.set(newConf)


def viewResponse(data, **kwargs):
    return Response(body=data, content_type='text/html', **kwargs)


def jsonResponse(data, **kwargs):
    data = json.dumps(data)
    return Response(body=data, content_type='application/json', **kwargs)
