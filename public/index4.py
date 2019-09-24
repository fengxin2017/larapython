import os
import sys

sys.path.append('/larapy/venv/Lib/site-packages')
sys.path.append('../')

# from config import app
from laravel.Illuminate.Helps.Help import *

from werkzeug.wrappers import Request as BaseRequest
from werkzeug.wrappers import Response as BaseResponse

from app.Http.Kernel import Kernel

from laravel.Illuminate.Http.Request import Request


# import select
# import socket
#
# response = b'HTTP/1.1 200 OK\r\nConnection: Close\r\nContent-Length: 11\r\n\r\nHello World'
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(False)
# server_address = ('0.0.0.0', 80)
# server.bind(server_address)
# server.listen(1024)
# READ_ONLY = select.EPOLLIN | select.EPOLLPRI
# epoll = select.epoll()
# epoll.register(server, READ_ONLY)
# timeout = 60
# fd_to_socket = { server.fileno(): server}
# while True:
#     Events = epoll.poll(timeout)
#     for fd, flag in Events:
#         sock = fd_to_socket[fd]
#         if flag & READ_ONLY:
#             if sock is server:
#                 conn, client_address = sock.accept()
#                 conn.setblocking(False)
#                 fd_to_socket[conn.fileno()] = conn
#                 epoll.register(conn, READ_ONLY)
#             else:
#                 request = sock.recv(1024)
#                 sock.send(response)
#                 sock.close()
#                 del fd_to_socket[fd]

# import socket
#
#
# server = socket.socket()
# server.bind(('0.0.0.0', 80))
# server.listen(1024)
#
# while True:
#     client, clientaddr = server.accept()  # blocking
#     request = client.recv(1024)  # blocking
#     client.send(b'HTTP/1.1 200 OK\r\nConnection: Close\r\nContent-Length: 11\r\n\r\nHello World')  # maybe blocking
#     client.close()

# LARAVEL_START = int(time.time() * 1000);

class Server(object):
    def __init__(self, kernel):
        self.kernel = kernel

    def wsgi_app(self, environ, start_response):
        # response = BaseResponse('hello world')
        # return response(environ, start_response)
        # request = BaseRequest(environ)
        if BaseRequest(environ).path == '/favicon.ico':
            response = BaseResponse('ico')
        else:

            request = Request(BaseRequest(environ))

            response = self.kernel.handle(request);

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


# def serve(with_static=True):
#     server = Server()
#     if with_static:
#         server.wsgi_app = SharedDataMiddleware(server.wsgi_app, {
#             '/static': os.path.join(os.path.dirname(__file__), 'static')
#         })
#     return server

def getKernelClosure(router):
    def closure(app):
        return Kernel(app, router)

    return closure


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    application = Application(os.getcwd() + '/../')

    application.singleton('kernel', getKernelClosure(app('router')))

    kernel = app('kernel').bootstrap()

    server = Server(kernel)

    run_simple('0.0.0.0', 80, server, use_debugger=True, use_reloader=True, threaded=True)


#
# response.send()
#
# exit()
#
#
# def main():
#     exit()
#
#     application.rebinding('instance', rebindInstance())
#
#     application.instance('instance', 'INSTANCE')
#
#     application.instance('instance', 'INSTANCE1')
#
#     exit()
#
#     Events = application.make('Events')
#
#     Events.listen('test', fn())
#
#     e = 'test'
#
#     name = 'foxriver'
#
#     age = 29
#
#     for i in range(10):
#         t = Thread(target=notifyWorker, args=(Events, e, name, age))
#         t.start()
#
#     exit()
#
#     app.singleton('kernel', Kernel())
#
#     print(app.ServiceProviders, app.bindings)
#
#
# def getKernelClosure():
#     def closure(app, router):
#         return Kernel(app, router)
#
#     return closure
#
#
# def bindClo():
#     def closure(app):
#         return 'test'
#
#     return closure
#
#
# def rebindInstance():
#     def closure(app, instance):
#         print('this is instance rebinding', app, instance)
#
#     return closure
#
#
# def rebindFn():
#     def closure(app, instance):
#         print(app, instance)
#
#     return closure
#
#
# def notifyWorker(Events, e, name, age):
#     Events.dispatch(e, name, age)
#
#
# def test():
#     print('111')
#
#
# def fn():
#     def test(name, age):
#         time.sleep(1)
#         print('name is ' + name + ' age is ' + str(age))
#
#     return test
#
#
# if __name__ == '__main__':
#     main()
