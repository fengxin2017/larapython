from app.Http.Controllers.Controller import Controller
from laravel.Helps.Help import app, jsonResponse, viewResponse
class PostController(Controller):
    def __init__(self):
        pass

    async def index(self,request):
        return viewResponse('<h1>Postcontroller@index</h1>')