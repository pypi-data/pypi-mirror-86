from mitama.app import Controller
from mitama.app.http import Response
from .model import *
import json
from datetime import datetime

class HomeController(Controller):
    def handle(self, request):
        template = self.view.get_template('index.html')
        j = json.dumps(request.user.to_dict())
        return Response.render(template, {
            'user_json': j
        })

class BoardController(Controller):
    def group(self, request):
        id = request.params['id']
        group = Group.retrieve(int(id))
        boards = Board.query.filter(Board.group == group)
        return Response.json(list([board.to_dict() for board in boards]))
    def user(self, request):
        id = request.params['id']
        user = User.retrieve(int(id))
        boards = [bg.board for bg in BoardGuest.query.filter(BoardGuest.user == user).all()]
        return Response.json(list([board.to_dict() for board in boards]))
    def list(self, request):
        boards = Board.query.filter(Board.group == None)
        return Response.json(list([board.to_dict() for board in boards]))
    def retrieve(self, request):
        board = Board.retrieve(request.params['id'])
        since = request.query.get('since', [None])[0]
        return Response(
            text = json.dumps(
                dict(
                    board.to_dict(),
                    posts = [post.to_dict() for post in board.posts(since)],
                    members = [user.id for user in board.members()],
                )
            ),
            content_type = 'application/json'
        )
    def create(self, request):
        post = request.post()
        board = Board()
        board.subject = post['subject']
        group = Group.retrieve(int(post['group'])) if 'group' in post else None
        board.group = group
        board.private = 'private' in post
        board.description = post.get('description', None)
        board.create()
        return Response.json({
            "_id": board._id
        })
    def update(self, request):
        post = request.post()
        board = Board.retrieve(request.params['id'])
        board.subject = post.get('subject', board.subject)
        board.description = post.get('description', board.description)
        board.private = post.get('private', board.private)
        board.group = post.get('group', board.group)
        return Response(
            text = json.dumps(
                board.to_dict()
            ),
            content_type = 'application/json'
        )
    def delete(self, request):
        board = Board.retrieve(request.params['id'])
        board.delete()
        return Response(
            text = json.dumps({}),
            content_type = 'application/json'
        )

class PostController(Controller):
    def create(self, request):
        data = request.post()
        post = Post()
        post.board = Board.retrieve(int(request.params['id']))
        post.user = request.user
        post.content = data['content']
        post.modified = datetime.now()
        post.posted = datetime.now()
        post.create()
        return Response(
            text = json.dumps({
                "_id": post._id
            }),
            content_type = 'application/json'
        )
    def update(self, request):
        data = request.post()
        post = Post.retrieve(int(request.params['pid']))
        post.content = data['content']
        post.modified = datetime.now()
        post.update()
        return Response(
            text = template,
            content_type = 'application/json'
        )
    def delete(self, request):
        post = Post.retrieve(int(request.params['pid']))
        post.delete()
        return Response(
            text = template,
            content_type = 'application/json'
        )
