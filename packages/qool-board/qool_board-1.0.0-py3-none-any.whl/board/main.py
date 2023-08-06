from mitama.app import App, Router
from mitama.utils.controllers import static_files
from mitama.utils.routers import retrieve_api_router
from mitama.utils.middlewares import SessionMiddleware
from .controller import *
from mitama.app.method import *


class App(App):
    name = 'QOOL Board'
    description = '情報の整理とスムーズな議論を両立するチャットシステム'
    router = Router([
        group('/api', Router([
            post('/boards', BoardController, 'create'),
            get('/boards', BoardController, 'list'),
            get('/boards/<id>', BoardController, 'retrieve'),
            put('/boards/<id>', BoardController, 'update'),
            delete('/boards/<id>', BoardController, 'delete'),
            post('/boards/<id>', PostController, 'create'),
            delete('/boards/<id>/<pid>', PostController, 'delete'),
            put('/boards/<id>/<pid>', PostController, 'update'),
            retrieve_api_router(),
            get('/groups/<id>/boards', BoardController, 'group'),
            get('/users/<id>/boards', BoardController, 'user'),
        ])),
        view('/static/<path:path>', static_files()),
        view('/<path:re:(.*)>', HomeController),
    ], middlewares = [SessionMiddleware])
