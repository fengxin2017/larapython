import asyncio
import json
import random

from app.Http.Controllers.Controller import Controller
from app.Jobs.FooJob import FooJob
from laravel.Helps.Help import viewResponse, jsonResponse
from laravel.Http.Response import Response


class HomeController(Controller):
    async def foo(self, request):
        # await asyncio.sleep(1)
        return viewResponse('this is homecontroller@foo')

    async def qiniu(self,request):
        ak = 'cXuruOsjHdk6kVGu4lVx7izG1O96ZyK8lis32ZDG'
        sk = 'a7em2JOptQXuD6Hf85DsOLjHjBlvLjC6DhmxzRef'
        from qiniu import Auth, put_file, etag
        from laravel.Helps.Help import app
        q = Auth(ak, sk)
        # 要上传的空间
        bucket_name = 'larapy'
        # 上传后保存的文件名
        key = 'laray6666.jpg'
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)
        # 要上传文件的本地路径
        localfile = app().staticPath + 'laravel/laravel.jpg'

        # print(localfile)

        ret, info = put_file(token, key, localfile)

        # print(info)

        return viewResponse('done')

    async def index(self, request):
        name = 'admin'
        age = 28
        str1 = '<h2>this is {} and i am {}</h2>'.format(name, age)
        d = json.dumps({'message': 'u dont have premission to access this url'})
        # request = app('request')
        # print(request.headers)
        # await asyncio.sleep(1)

        #
        # data = await crequest().post()
        # print(data)

        # print(await current_request('age'))
        # print(await current_request('name'))

        # 上传
        file = await request.files('image')

        path = file.storeAs('laravel', 'laravel')


        # request.files('image').store()
        # img = await current_request('image',method='POST')
        # print(img)
        # content = img.file.read()
        #
        # with open(app().storagePath + '1.jpg','wb') as f:
        #     f.write(content)

        # req = await current_request()
        #
        # print(req.get())
        # print(await req.posts())
        # print(await req.all())
        # print(request.get())
        # print(await request.posts())
        # print(await request.all())

        # req = await current_request()
        # print(req.headers)

        # print(id(capp('Redis')))
        # print(crequest().query['name'])
        # print(config('Queue.message'))
        # print(currentConfig.get().get('Queue.message'))
        return jsonResponse({'path': path})
        return Response(body=d, status=200, content_type='application/json')
        return Response(body=str1, status=200, content_type='text/html')
        # return Response.json(d,status=200,mimetype='application/json')
        # return Response(d, status=200, mimetype='application/json')
        # return Response(d, status=200, mimetype='application/json')
        # return Response(str, status=200, mimetype='text/html')

    async def home(self, request):
        # return viewResponse('<h1>ahahahahhahah</h1>', status=200)
        # return jsonResponse({'name': 'admin', 'age': 30})
        name = request.request.query['name']
        age = request.request.query['age']
        html = '<h2>this is {name} and i am {age}.'.format(name=name, age=age)
        return viewResponse(html, status=200)

    async def queue(self, request):
        for i in range(10, 20, 3):
            # FooJob.dispatch({
            #     'name': 'admin' + str(i) + '|' + str(random.randint(1, 100000))
            # })
            # FooJob.dispatch({
            #     'name': 'admin' + str(i) + '|' + str(random.randint(1, 100000))
            # })
            # FooJob.dispatch({
            #     'name': 'admin' + str(i) + '|' + str(random.randint(1, 100000))
            # })
            # FooJob.dispatch({
            #     'name': 'admin' + str(i) + '|' + str(random.randint(1, 100000))
            # })

            # 延迟队列
            FooJob.dispatch({
                'name': 'admin' + str(i) + '|' + str(random.randint(1, 100000))
            }).onQueue('default').delay(i)
            FooJob.dispatch({
                'name': 'admin' + str(i) + '|' + str(random.randint(1, 100000))
            }).onQueue('default').delay(i)
            FooJob.dispatch({
                'name': 'admin' + str(i) + '|' + str(random.randint(1, 100000))
            }).onQueue('default').delay(i)
            FooJob.dispatch({
                'name': 'admin' + str(i) + '|' + str(random.randint(1, 100000))
            }).onQueue('default').delay(i)

        return Response(text='done', status=200, content_type='text/html')
        # return viewResponse('queued!')
