from mitama.db import BaseDatabase
from mitama.db.types import *
from mitama.models import *
from datetime import datetime
import dateutil.parser
from tzlocal import get_localzone

class Database(BaseDatabase):
    pass

db = Database()

class Board(db.Model):
    subject = Column(String)
    description = Column(String)
    private = Column(Boolean, default = False)
    group = Column(Group.type)
    def members(self):
        members = list()
        for user in BoardGuest.query.filter(BoardGuest.board == self):
            if user not in members: members.append(user)
        if self.group is not None:
            for node in self.group.children():
                if isinstance(node, Group): continue
                if node not in members: members.append(node)
        return members
    def posts(self, since = None):
        since = dateutil.parser.parse(since).astimezone(get_localzone()) if since is not None else datetime.fromtimestamp(0)
        since = since or datetime.fromtimestamp(0)
        posts = Post.query.filter(Post.board == self, Post.modified > since).all()
        return posts
    def delete(self):
        db.session.start()
        Post.query.filter(Post.board == self).delete()
        BoardGuest.query.filter(Post.board == self).delete()
        db.query.delete(self)
        db.session.commit()
    def to_dict(self):
        return {
            "_id": self._id,
            "subject": self.subject,
            "description": self.description,
            "private": self.private,
            "group": {
                "id": self.group.id,
                "name": self.group.name,
                "screen_name": self.group.screen_name,
                "icon": self.group.icon_to_dataurl()
            } if self.group is not None else None
        }

class Post(db.Model):
    board = Column(Board.type)
    user = Column(User.type)
    posted = Column(DateTime)
    modified = Column(DateTime)
    content = Column(String)
    def to_dict(self):
        return {
            "_id": self._id,
            "board": self.board._id,
            "posted": self.posted.isoformat(),
            "modified": self.modified.isoformat(),
            "content": self.content,
            "user": {
                "id": self.user.id,
                "name": self.user.name,
                "screen_name": self.user.screen_name,
                "icon": self.user.icon_to_dataurl()
            }
        }

class BoardGuest(db.Model):
    board = Column(Board.type)
    user = Column(User.type)

db.create_all()
